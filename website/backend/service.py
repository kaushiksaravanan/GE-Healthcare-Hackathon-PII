import json

import MySQLdb
from database import SERVER, USERNAME, PASSWORD, DATABASE, REDACTION_TABLE, DOCUMENT_TABLE, ENTITY_TABLE, USERS_TABLE, ACCESS_RIGHTS_TABLE

def insert_into_redaction_table(identified, entity_type, redact, is_replaced, document_id):
    # print("DEBUG:")
    # print("Insert Redaction Table")
    # TODO: To handle 'John Doe's' when insertion.
    # print("Redact: ", redact)
    redact = redact.replace("'", "''")
    sql = "INSERT INTO " + REDACTION_TABLE + " (identified, entity_type, redact, is_replaced, document_id) VALUES ('" + identified + "', '" + entity_type + "', '" + redact + "', " + str(is_replaced) + ", " + str(document_id) + ")"
    # print(sql)
    # cursor.execute(sql)
    # db.commit()
    
def insert_into_application_statistics_table(files,words,no_pii,time_taken):
    try:
        db = MySQLdb.connect(SERVER, USERNAME, PASSWORD, DATABASE)
        cursor = db.cursor()
        
        cursor.execute("SELECT no_of_files, no_of_words, no_of_pii, no_of_time FROM application_statistics_table WHERE id=1")
        current_data = cursor.fetchone()

        no_of_files, no_of_words, no_of_pii, no_of_time = current_data
        updated_files=no_of_files+files
        updated_words=no_of_words+words
        updated_pii_count=no_of_pii+no_pii
        updated_time=no_of_time+time_taken
        
        sql = f"""UPDATE application_statistics_table 
        SET no_of_files = {updated_files}, 
            no_of_words = {updated_words}, 
            no_of_pii = {updated_pii_count}, 
            no_of_time = {updated_time} 
        WHERE id=1;
        """
        cursor.execute(sql)
        db.commit()
        db.close()
        return 0
    except:
        print("Error")
        return 1

def insert_into_document_table(document_name, document_size, timestamp, processed_time, data_input, data_output, highlight_text, replaced_value_dict, detection_type, owner_id):
    # print("DEBUG:")
    # print("Insert Document Table")
    try:
        db = MySQLdb.connect(SERVER, USERNAME, PASSWORD, DATABASE)
        cursor = db.cursor()
        sql = "INSERT INTO " + DOCUMENT_TABLE + " (document_name, document_size, timestamp, processed_time, data_input, data_output, highlight_text, replaced_value_dict, detection_type, owner_id) VALUES ('" + str(document_name) + "', " + str(document_size) + ", '" + str(timestamp) + "', " + str(processed_time) + ", " + json.dumps(str(data_input)) + ", " + json.dumps(str(data_output)) + ", " + json.dumps(str(highlight_text)) + ", " + json.dumps(str(replaced_value_dict)) + ", '" + str(detection_type) + "', " + str(owner_id) + ")"
        print(sql)
        print(replaced_value_dict)
        cursor.execute(sql)
        last_row_id = cursor.lastrowid
        cursor.close()
        db.commit()
        return last_row_id
    except:
        print("Error")
        return 1
    # return 1

def insert_into_entity_table(user_id, entity_id, list_of_documents):
    # print("DEBUG:")
    # print("Insert Entity Table")
    sql = "INSERT INTO " + ENTITY_TABLE + " (user_id, entity_id, list_of_documents, is_updated) VALUES (" + str(user_id) + ", " + str(entity_id) + ", ' ', 0)"
    # print(sql)

def update_entity_table(owner_id, document_id):
    # print("DEBUG:")
    # print("Update Entity Table")
    sql = "UPDATE " + ENTITY_TABLE + " SET list_of_documents = CONCAT(list_of_documents, '" + str(document_id) +" ') WHERE is_processed = 0 AND user_id = " + str(owner_id) + ""
    # print(sql)

def insert_into_users_table(user_name, user_email, user_password):
    # print("Users Table")
    sql = "INSERT INTO " + USERS_TABLE + " (user_name, user_email, user_password) VALUES ('" + str(user_name) + "', '" + str(user_email) + "', '" + str(user_password) + "')"
    print(sql)
    # cursor.execute(sql)
    # last_row_id = cursor.lastrowid
    # return last_row_id
    # Return the user id to login
    return 1

def insert_into_access_rights_table(user_id, document_id, access_id):
    # print("Access Rights Table")
    sql = "INSERT INTO " + ACCESS_RIGHTS_TABLE + " (user_id, document_id, access_id) VALUES (" + str(user_id) + ", " + str(document_id) + ", " + str(access_id) + ")"
    # print(sql)

def update_access_rights_table(user_id, document_id, access_id):
    sql = "UPDATE " + ACCESS_RIGHTS_TABLE + " SET access_id = " + str(access_id) + " WHERE user_id = " + str(user_id) + " AND document_id = " + str(document_id) + ""
    # print(sql)