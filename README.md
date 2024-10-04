# Visa Prediction Project with MLOps Implementation

Welcome to the **Visa Prediction Project**! This project combines the power of Data Science and MLOps to automate the prediction of visa application approval or rejection. By leveraging MLOps practices, we ensure efficient model development, deployment, and monitoring, resulting in a robust and scalable solution.
## 1 Problem statement.

* OFLC gives job certification applications for employers seeking to bring foreign workers into the United States and grants certifications. 
* As In last year the count of employees were huge so OFLC needs Machine learning models to shortlist visa applicants based on their previous data.

**In this project we are going to use the data given to build a Classification model:**

* This model is to check if Visa get approved or not based on the given dataset.
* This can be used to Recommend a suitable profile for the applicants for whom the visa should be certified or denied based on the certain criteria which influences the decision.
### About
The Immigration and Nationality Act (INA) of the US permits foreign workers to come to the United States to work on either a temporary or permanent basis. 
The act also protects US workers against adverse impacts on working place and maintain requirements when they hire foreign workers to fill workforce shortages. The immigration programs are administered by the Office of Foreign Labor Certification (OFLC).

## Overview
The Visa Prediction Project utilizes machine learning algorithms to predict visa approval or rejection. The project focuses on implementing an end-to-end MLOps pipeline to manage the entire lifecycle of the model, from development to deployment and maintenance.

## Features
- **Data Ingestion**: Load and store visa application data from external sources into MongoDB Atlas.
- **Exploratory Data Analysis (EDA)**: Generate meaningful insights from the data and perform feature engineering.
- **Data Validation**: Ensure that the input data is clean and reliable.
- **Data Transformation**: Preprocess and normalize data to make it suitable for model training.
- **Model Training**: Train machine learning models, perform hyperparameter tuning, and use cross-validation.
- **Model Evaluation**: Evaluate model performance with various metrics and choose the best one for deployment.
- **Deployment**: Automate model deployment using Docker and AWS EC2, and store Docker images in ECR (Elastic Container Registry).
- **CI/CD Pipeline**: Enable continuous integration and deployment with GitHub Actions and AWS, ensuring seamless updates.

## Project Structure

```plaintext
├── data_ingestion/         # Scripts for data ingestion into MongoDB Atlas
├── eda/                    # Notebooks for EDA and Feature Engineering
├── data_validation/        # Scripts for data validation
├── data_transformation/    # Data preprocessing and transformation scripts
├── model_training/         # Model training and hyperparameter tuning scripts
├── model_evaluation/       # Model evaluation components
├── deployment/             # Deployment scripts and Dockerfiles
├── cicd/                   # CI/CD pipeline configuration
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```


## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Syed-Mansoor/MLOps-AWS-CICD-US-Visa-Approval-Prediction.git
cd MLOps-AWS-CICD-US-Visa-Approval-Prediction
```
## 2. Setup python environment
#### 1.Create a virtual environment and install the dependencies:

``` conda
conda create -p .usvisa python=3.8 -y
conda activate .usvisa
pip install -r requirements.txt
```
#### 2.Install Docker if not already installed:
``` bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```
## 3. MongoDB Atlas Configuration
- Setup a MongoDB Atlas account and connect your database.
- Update the connection string in your environment configuration file.
## 4. AWS Setup for Deployment
### 1. Login to AWS Console and Create an IAM User
Grant the IAM user access to:

- EC2 (Virtual Machine)
- ECR (Elastic Container Registry for Docker Images)
### 2. AWS Policies
Assign the following policies to your IAM user:

- AmazonEC2ContainerRegistryFullAccess
- AmazonEC2FullAccess
### 3. Create ECR Repository
- Create an ECR repo to store the Docker image.
- Save the ECR URI for later use:
315865595366.dkr.ecr.us-east-1.amazonaws.com/visarepo
### 4. Build and Push Docker Image to ECR
``` bash
# Build the Docker image
docker build -t visa-prediction .

# Tag the Docker image
docker tag visa-prediction:latest 315865595366.dkr.ecr.us-east-1.amazonaws.com/visarepo:latest

# Push the image to ECR
docker push 315865595366.dkr.ecr.us-east-1.amazonaws.com/visarepo:latest

```
### 5. Launch EC2 Instance and Pull Docker Image
1. Launch an EC2 instance (Ubuntu).

2. SSH into the EC2 instance and install Docker:

```bash
sudo apt-get update -y
sudo apt-get install docker.io
sudo usermod -aG docker $USER
```
3. Pull the Docker image from ECR and run it:

``` bash
docker pull 315865595366.dkr.ecr.us-east-1.amazonaws.com/visarepo:latest
docker run -d -p 5000:5000 visa-prediction
```
### 6. CI/CD Pipeline with GitHub Actions
This project uses GitHub Actions to automate the deployment process:

1. Setup GitHub Secrets:

- Add the following secrets in your GitHub repository settings:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_DEFAULT_REGION
    - ECR_REPO
2. Configure Self-hosted Runner:

    - Go to your repository → Settings → Actions → Runners.
    - Set up the runner by following the instructions for your EC2 instance.
3. Configure GitHub Actions Workflow:

    - The .github/workflows folder contains configuration files for the CI/CD pipeline.
    - The pipeline automatically builds, tests, and deploys the application with every code update.
# Technologies Used
- Python for machine learning and data processing
- MongoDB Atlas for database management
- AWS EC2 for model deployment
- AWS ECR for storing Docker images
- Docker for containerization
- GitHub Actions for CI/CD pipeline automation
# License
This project is licensed under the MIT License.







