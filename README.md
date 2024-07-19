# Streamlit App with Pinecone Integration

This project is a Streamlit application that allows users to filter a dataset and perform query searches using Pinecone. The app is containerized using Docker and can be easily managed with Docker Compose.

## Features

- Filter data by industry and country
- Perform query searches using Pinecone
- Secure access with password protection
- Containerized for easy deployment

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/your_username/your_repository.git
    cd your_repository
    ```

2. Create a `.env` file with your environment variables:
    ```plaintext
    PINECONE_API_KEY=your_pinecone_api_key
    PINECONE_INDEX_NAME=your_pinecone_index_name
    APP_PASSWORD=your_application_password
    ```

3. Ensure your directory structure looks like this:
    ```
    your_project/
    ├── app.py
    ├── Dockerfile
    ├── requirements.txt
    ├── docker-compose.yml
    ├── .env
    └── data/
        └── sample_with_descriptions.csv
    ```

4. Build and run the Docker container:
    ```sh
    docker-compose up --build
    ```

5. Open your browser and go to `http://localhost:8501` to access the Streamlit app.

## Files

- `app.py`: The main Streamlit application code.
- `Dockerfile`: Instructions to build the Docker image.
- `requirements.txt`: List of Python dependencies.
- `docker-compose.yml`: Docker Compose configuration.
- `.env`: Environment variables for the application.
- `data/sample_with_descriptions.csv`: Sample dataset file.

## Usage

- **Filter Options**: Use the sidebar to filter the dataset by industry and country.
- **Query Search**: Enter a query in the sidebar and provide the correct password to perform a search using Pinecone.
- **Top-k Results**: Select the number of top-k results to retrieve (maximum 100).

## Environment Variables

Ensure you have the following environment variables set in your `.env` file:

- `PINECONE_API_KEY`: Your Pinecone API key.
- `PINECONE_INDEX_NAME`: The name of your Pinecone index.
- `APP_PASSWORD`: The password to access the query search feature.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
