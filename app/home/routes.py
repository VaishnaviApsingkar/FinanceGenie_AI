from flask import Blueprint, render_template, request, jsonify, flash 
from flask_login import current_user,login_required
from sqlalchemy.sql import text
from werkzeug.utils import secure_filename
from sqlalchemy import inspect
import datetime

#for AI agent
import openai
from PIL import Image
import pytesseract
import pdfplumber
import os
from dotenv import load_dotenv
from flask import current_app
import json
import re


from ..models import BankAccount
from ..models import db
from . import home_bp



# home_bp = Blueprint('home', __name__)

@home_bp.route('/dashboard', methods=['GET'])
def dashboard():
    accounts = BankAccount.query.filter_by(user_id=current_user.id).all()  # Replace with logged-in user ID
    return render_template('home.html', accounts=accounts)

@home_bp.route('/api/add_account', methods=['POST'])
# @login_required
def add_account():
    data = request.get_json()
    bank_name = data.get('bank_name')
    account_nickname = data.get('account_nickname')
    account_number = data.get('account_number')
    balance = data.get('balance')

     # Validate input data
    if not all([bank_name, account_nickname, account_number, balance]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        new_account = BankAccount(
            user_id=current_user.id,
            bank_name=bank_name,
            account_nickname=account_nickname,
            account_number=account_number,
            balance=balance
        )
        db.session.add(new_account)
        db.session.commit()
        return jsonify({"message": "Account added successfully"}), 201
    except Exception as e:
        print(f"Error adding account: {e}")
        return jsonify({"error": "An error occurred while adding the account"}), 500


@home_bp.route('/api/delete_account/<int:account_id>', methods=['DELETE'])
# @login_required
def delete_account_and_table(account_id):
    # Fetch the bank account
    account = BankAccount.query.filter_by(id=account_id, user_id=current_user.id).first()
    if account:
        # Generate the transaction table name
        table_name = f"{account.account_nickname}_transactions"

        # Drop the associated transaction table
        try:
            db.session.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            db.session.commit()
        except Exception as e:
            return jsonify({"message": f"Failed to delete transaction table: {str(e)}"}), 500

        # Delete the bank account
        db.session.delete(account)
        db.session.commit()

        return jsonify({"message": "Account and associated transaction table deleted successfully"}), 200
    else:
        return jsonify({"message": "Account not found"}), 404

@home_bp.route('/api/get_accounts', methods=['GET'])
@login_required
def get_accounts():
    """API endpoint for retrieving all bank accounts for the logged-in user."""
    accounts = BankAccount.query.filter_by(user_id=current_user.id).all()
    accounts_list = [
        {
            "id": account.id,
            "bank_name": account.bank_name,
            "account_nickname": account.account_nickname,
            "account_number": account.account_number,
            "balance": account.balance
        } for account in accounts
    ]
    return jsonify(accounts_list), 200

#Code for AI agent
load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path



# Database setup (import your existing db instance)

# 1. Retrieve Schema for bank_account Table
def get_bank_account_schema():
    """
    Retrieve the schema for the 'bank_account' table.
    """
    inspector = inspect(db.engine)
    columns = inspector.get_columns("bank_account")
    schema_info = {
        "table_name": "bank_account",
        "columns": [{"name": col["name"], "type": str(col["type"])} for col in columns]
    }
    return schema_info

# 2. Retrieve Schema for User-Specific Transaction Table
def get_user_transaction_schema():
    """
    Retrieve schema details for the logged-in user's transaction table.
    """
    if not current_user.is_authenticated:
        raise ValueError("User is not authenticated")
    
    table_name = current_user.transaction_table_name  # Get user-specific table name
    inspector = inspect(db.engine)

    # Check if the table exists
    if table_name not in inspector.get_table_names():
        raise ValueError(f"Table {table_name} does not exist for the current user")

    # Get column details for the table
    columns = inspector.get_columns(table_name)
    schema_info = {
        "table_name": table_name,
        "columns": [{"name": col["name"], "type": str(col["type"])} for col in columns]
    }
    return schema_info

# 3. Combine and Format Schema for OpenAI
def format_combined_schema():
    """
    Format the combined schema for OpenAI.
    """
    try:
        # Retrieve schemas
        bank_account_schema = get_bank_account_schema()
        user_transaction_schema = get_user_transaction_schema()

        # Format schemas
        formatted_schema = "Database Schema:\n\n"
        for schema in [bank_account_schema, user_transaction_schema]:
            formatted_schema += f"Table: {schema['table_name']}\nColumns:\n"
            for column in schema["columns"]:
                formatted_schema += f"  - {column['name']} ({column['type']})\n"
            formatted_schema += "\n"

        return formatted_schema
    except Exception as e:
        return f"Error retrieving schema: {str(e)}"

#4. get current user account details.
def get_user_bank_accounts():
    """
    Retrieve bank account details (bank_id, account_nickname, account_number) for the current logged-in user.
    """
    if not current_user.is_authenticated:
        raise ValueError("User is not authenticated")

    # Query bank accounts for the current user
    bank_accounts = BankAccount.query.filter_by(user_id=current_user.id).all()

    # Format the bank account details
    account_details = [
        {
            "bank_id": account.id,
            "bank_name": account.bank_name,
            "account_nickname": account.account_nickname,
        }
        for account in bank_accounts
    ]

    return account_details

# File Parsing Function:
# def parse_file(file):
#     """Extract text from PDF, image, or text files."""
#     if file.filename.endswith('.pdf'):
#         with pdfplumber.open(file) as pdf:
#             return ''.join(page.extract_text() for page in pdf.pages)
#     elif file.filename.endswith(('.png', '.jpg', '.jpeg')):
#         image = Image.open(file)
#         return pytesseract.image_to_string(image)
#     elif file.filename.endswith('.txt'):
#         return file.read().decode('utf-8')
#     else:
#         raise ValueError("Unsupported file format")

# File Parsing Function:
def parse_file(file):
    """
    Extract text from PDF, image, or text files.
    """
    if isinstance(file, str):  # If file is a file path (string)
        file_extension = os.path.splitext(file)[1].lower()
        if file_extension == '.pdf':
            with pdfplumber.open(file) as pdf:
                return ''.join(page.extract_text() for page in pdf.pages)
        elif file_extension in ('.png', '.jpg', '.jpeg'):
            image = Image.open(file)
            return pytesseract.image_to_string(image)
        elif file_extension == '.txt':
            with open(file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError("Unsupported file format")
    elif hasattr(file, 'filename'):  # If file is an uploaded file object
        if file.filename.endswith('.pdf'):
            with pdfplumber.open(file) as pdf:
                return ''.join(page.extract_text() for page in pdf.pages)
        elif file.filename.endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(file)
            return pytesseract.image_to_string(image)
        elif file.filename.endswith('.txt'):
            return file.read().decode('utf-8')
        else:
            raise ValueError("Unsupported file format")
    else:
        raise ValueError("Invalid file input")
    
def generate_sql_query(prompt, schema, extracted_data):
    # openai.api_key = "your_openai_api_key"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"database schema:\n{schema} Generate only the SQL query,No text,comments,or code blocks. Output must be raw SQL only"},
            {"role": "user", "content": f"{prompt}\nExtracted data:\n{extracted_data}"}
        ],
        max_tokens=200
    )
    return response['choices'][0]['message']['content'].strip()

# def summarize_query_results(results, column_names):

#     # Validate the results and column_names
#     if not results or not column_names:
#         return "No results found to summarize."
    
#     # Convert query results into a list of dictionaries
#     try:
#         result_data = [dict(zip(column_names, row)) for row in results]
#     except Exception as e:
#         return f"Error processing query results: {str(e)}"
    
#     # Debugging: Log result_data to confirm structure
#     print(f"Result Data for Summarization: {result_data}")

#     # Generate summary using OpenAI 
#     openai.api_key = os.getenv("OPENAI_API_KEY")
    
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are data analyst.Summarize query results in natural language"},
#             {"role": "user", "content": f"Query results:\n{json.dumps(result_data, indent=2)}"}
#         ],
#         max_tokens=150
#     )
#     return response['choices'][0]['message']['content'].strip()

def summarize_query_results(prompt, result_data):

    # Validate the results and column_names
    if not result_data:
        return "No results found to summarize."
       
    # Debugging: Log result_data to confirm structure
    print(f"Result Data for Summarization: {result_data}")

    # Generate summary using OpenAI 
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are data analyst.Summarize data in natural language"},
            {"role": "user", "content": f"{prompt}Query results:\n{json.dumps(result_data, indent=2)}"}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

def execute_sql_query(sql_query):
    """Execute a SQL query and return results."""
    connection = db.engine.connect()
    trans = connection.begin()  # Start a transaction

    try:
        result = connection.execute(text(sql_query))
        print(f"Result of execute sql query: {result}")
        # if result.returns_rows:
        #     rows = result.fetchall()
        #     column_names = result.keys()
        #     print("Column Names:", column_names)
        #     print("Rows:", rows)
        #     return rows, column_names
        if not result.returns_rows:
            trans.commit()  # Commit for INSERT/UPDATE/DELETE
            print("Transaction committed successfully.")
        else:
            rows = result.fetchall()
            column_names = result.keys()
            print("Query returned rows:", rows)
            return rows, column_names
        
        return [], []
    except Exception as e:
        trans.rollback()  # Rollback in case of errors
        
        raise ValueError(f"Error executing SQL query: {e}")
    finally:
        connection.close()

# def parse_prompt_to_transaction_and_account(prompt):
    """Use AI to interpret user prompt and extract transaction and account data."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "get transaction details like (account_nickname, transaction_date yyyy-mm-dd, amount, type, transaction_name, transaction_id) in json format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        message_content = response.choices[0].message['content'].strip()  # Process response as needed
        print(f"message_content:{message_content}")

        # Clean the response (e.g., remove code block markers if present)
        cleaned_response = message_content.replace("```json", "").replace("```", "").strip()
        # cleaned_response = message_content.strip('```json').strip('```').strip()
        print(f"cleaned_response:{cleaned_response}")
        if not cleaned_response:
            raise ValueError("OpenAI response is empty or invalid.")

        try:
        # Match the JSON dictionary using regex
            json_match = re.search(r"{.*}", cleaned_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)  # Extract the JSON string
                parsed_data = json.loads(json_str)
                return parsed_data
            else:
                raise ValueError("No valid JSON dictionary found in the response")
        except Exception as e:
            print(f"Error extracting JSON: {e}")
            raise ValueError("Error extracting JSON")

    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        raise ValueError(f"Error parsing OpenAI response: {e}")

@home_bp.route('/api/process_file_and_add_transaction', methods=['POST'])
@login_required
def process_file_and_add_transaction():

    # Log database connection
    print(f"Database connection: {db.engine.url}")

    """
    Generate and execute a SQL query based on the user's prompt, schema, and optional file.
    """
    try:
        # Get user prompt and optional file
        prompt = request.form.get('prompt')
        file = request.files.get('file')

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        # Fetch user's bank account details
        user_accounts = get_user_bank_accounts()
        if not user_accounts:
            return jsonify({"error": "No bank accounts found for the current user"}), 400

        # Format account details for inclusion in the schema
        account_details_text = "\n".join(
            [
                f"- {account['bank_name']} (Nickname: {account['account_nickname']}, Bank ID: {account['bank_id']})"
                for account in user_accounts
            ]
        )

        # Process file if provided
        extracted_data = ""
        if file:
            # Save and process the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            print(f"Uploaded file: {file.filename}")
            print(f"Saved file to: {file_path}")

            # Extract text or relevant content from the file
            try:
                extracted_data = parse_file(file_path)  # Function to extract data from file
                print(f"Extracted Data: {extracted_data}")
            finally:
                # Ensure the file is removed after processing
                os.remove(file_path)

        # Get the combined schema for the logged-in user
        schema_text = format_combined_schema()
        if "Error" in schema_text:
            return jsonify({"error": schema_text}), 400
        
       
        print(f"prompt: {prompt}")
        print(f"schema_text : {schema_text}")
        print(f"extracted_data: {extracted_data}")
        print(f"account_data: {account_details_text}")

        # Append account details to schema for OpenAI query
        schema_with_accounts = f"{schema_text}\n\nUser's Bank Accounts:\n{account_details_text}"

        # Generate SQL query using OpenAI
        sql_query = generate_sql_query(prompt, schema_with_accounts, extracted_data)
        print(f"Generated SQL Query: {sql_query}")

        # Execute the SQL query
        results, column_names = execute_sql_query(sql_query)

        # Summarize the results if any
        # if results:
        #     result_data = [dict(zip(column_names, row)) for row in results]
        #     summary = summarize_query_results(result_data, column_names)
        #     # return jsonify({"summary": summary})
        #     print(f"Summary:{summary}")
        #     return summary
        
        # Summarize the results if any
        if results:
            # result_data = [dict(zip(column_names, row)) for row in results]
            result_data = [
                {k: (v.isoformat() if isinstance(v, (datetime.date, datetime.datetime)) else v) for k, v in dict(zip(column_names, row)).items()}
                for row in results
            ]
            summary = summarize_query_results(prompt, result_data)
            # return jsonify({"summary": summary})
            print(f"Summary:{summary}")
            return summary

        # return jsonify({"message": "Query executed successfully."})
        return "Action executed successfully. You can retrive transaction by asking 'details of last transaction'."
        

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500
