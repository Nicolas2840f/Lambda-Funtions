import json

def lambda_handler(event, context):
    print(event)
  
    # Mock data for demonstration purposes
    cv_data = [
        {"name": "John Doe", "role": "FullStack Developer", "experience": 5, "technologies": ["HTML", "CSS", "JavaScript", "React", "Node.js"], "salary_expectation": 11000},
        {"name": "Jane Smith", "role": "Backend Developer", "experience": 7, "technologies": ["Python", "Django", "Flask", "PostgreSQL"], "salary_expectation": 10000},
        {"name": "Alice Johnson", "role": "FrontEnd Developer", "experience": 4, "technologies": ["HTML", "CSS", "JavaScript", "Vue.js"], "salary_expectation": 8000},
        {"name": "Bob Brown", "role": "QA Engineer", "experience": 6, "technologies": ["Selenium", "JUnit", "Cypress"], "salary_expectation": 7000},
        {"name": "Charlie Davis", "role": "Technical Lead", "experience": 10, "technologies": ["Java", "Spring Boot", "Kubernetes"], "salary_expectation": 11000},
        {"name": "Diana Evans", "role": "Project Manager", "experience": 8, "technologies": ["Jira", "Scrum", "Kanban"], "salary_expectation": 9000}
    ]
    
    def get_named_parameter(event, name):
        return next(item for item in event['parameters'] if item['name'] == name)['value']
    
    def profile_cv(event):
        name = get_named_parameter(event, 'name').lower()
        for cv in cv_data:
            if cv["name"].lower() == name:
                return cv
        return None
    
    def query_cv_database(event):
        role = get_named_parameter(event, 'role').lower()
        filtered_cvs = [cv for cv in cv_data if cv['role'].lower() == role]
        return filtered_cvs
    
    def deliver_profiles_by_budget(event):
        budget = int(get_named_parameter(event, 'budget'))
        filtered_cvs = [cv for cv in cv_data if cv['salary_expectation'] <= budget]
        return filtered_cvs
    
    def deliver_profiles_by_need(event):
        role = get_named_parameter(event, 'role').lower()
        experience = int(get_named_parameter(event, 'experience'))
        technologies = get_named_parameter(event, 'technologies').split(', ')
        
        filtered_cvs = []
        for cv in cv_data:
            if (cv['role'].lower() == role and cv['experience'] >= experience and
                all(tech in cv['technologies'] for tech in technologies)):
                filtered_cvs.append(cv)
        
        return filtered_cvs
    
    def send_email(event):
        email_address = get_named_parameter(event, 'email_address')
        subject = get_named_parameter(event, 'subject')
        body = get_named_parameter(event, 'body')
        
        # Simulando el envío de un email
        print(f"Sending email to {email_address} with subject '{subject}' and body '{body}'")
        
        return "Email sent successfully"
      
    result = ''
    response_code = 200
    api_path = event['apiPath']
    
    if api_path == '/profileCV':
        result = profile_cv(event)
    elif api_path == '/queryCVDatabase':
        result = query_cv_database(event)
    elif api_path == '/deliverProfilesByBudget':
        result = deliver_profiles_by_budget(event)
    elif api_path == '/deliverProfilesByNeed':
        result = deliver_profiles_by_need(event)
    elif api_path == '/sendEmail':
        result = send_email(event)
    else:
        response_code = 404
        result = f"Unrecognized api path: {api_path}"
        
    response_body = {
        'application/json': {
            'body': result
        }
    }
        
    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': response_code,
        'responseBody': response_body
    }

    api_response = {'messageVersion': '1.0', 'response': action_response}
    return api_response
