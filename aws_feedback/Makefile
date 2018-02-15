all:
	#create zip package to upload to AWS
	zip -r aws.zip lambda_function.py

deploy:
	make all
	aws lambda update-function-code --function-name arn:aws:lambda:eu-west-1:285737895683:function:feedbackProcessing --zip-file fileb://./aws.zip
