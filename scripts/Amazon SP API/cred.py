
credentials = {
    "endpoint" : "https://sandbox.sellingpartnerapi-eu.amazon.com",
    "refreshtoken" : "Atzr|IwEBIHxmNG3NNehefJMUTcH03cW5t71RZOVlrrZTsPLM-lZyP1I48GHR0iwsJoE3wHNYSxYze_MT6f4e52x2mHxTn3fLk9ZP_OvYW3V1ooYw8CQS7G1GZnM_Vq7d_3Iwk6QjSvyY0M1h_hYyZkt83SQZbp7NL_rsXjTOJjHtrihkCWgzQKO8GyK9bFlzij18rJwTR5xm3jqv4tWkydie0g4p-5ET8NCp5Dt6ciKmJfwBFdiCNMTM5NLfZHZrAG33ACxqFMjx_C4Z7sYMgWDkOeyL8o_CPyAtqsGqhIrwV073EMrTUVg2uEDbUoFYzOLNxIlNkuPnNsce5Uz9wm_YoGb04EUS",
    "app_id" : "amzn1.sp.solution.5539b8b8-540d-436d-adfe-75eab1bd3eef",
    "client_id" : "amzn1.application-oa2-client.440003f0ec0f4742b8a4114a6f355adc",
    "client_secret" : "amzn1.oa2-cs.v1.3d5adf1e738e0d5ea9483c9f830ba8e304d253ff3f8d66692a1945",
    "access_token" : ""

}


state = "asdflkj"
seller_auth = f"https://sellercentral.amazon.com/apps/authorize/consent?application_id={credentials["app_id"]}&state={state}&version=beta"

print(seller_auth)