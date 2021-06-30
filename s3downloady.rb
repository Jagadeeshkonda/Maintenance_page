require 'json'
require 'aws-sdk-s3'


def lambda_handler(event:, context:)
    # TODO implement
    s3 = Aws::S3::Client.new
    resp = s3.get_object(bucket:'test.ls.co.uk', key:'maintenance.html')
    $body1= resp.body.read
    
    {
            statusCode: 200,
            isBase64Encoded: false,
            body: $body1 ,
            headers: {
                "Content-Type": "text/html; charset= utf-8"
            }
        }
end
