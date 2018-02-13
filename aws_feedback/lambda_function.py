def lambda_handler(event, context):
    from_page = event['from']
    to_page = event['to']
    feedback = event['feedback']
    
    message = "You are currently on the page " + from_page + "\nYou have given " + feedback + " feedback for the suggested page \n" + to_page
    return {"message": message}
