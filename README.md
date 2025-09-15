# Nutritionist

This is a Line OA with food nutritional analysis. Users can use this robot to obtain nutritional analysis of food for each day or meal.

## Run it

- If you want to run the robot locally with docker, please follow these steps.
  1. `touch .env`.
  2. Set the `CHANNEL_SECRET={your line channel secret}` in the `.env` file.
  3. Set the `CHANNEL_ACCESS_TOKEN={your line channel access token}` in the `.env` file.
  4. Set the `OPENAI_API_KEY={youe openai api key}` in the `.env` file.
  5. Run the `make service-up` command.
  6. Run the `make service-down` command if you want to end the service.
