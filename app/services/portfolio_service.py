class PortfolioService:

    def generate_projects(self, role: str):
        """
        Generate sample projects based on selected role
        """

        projects_data = {

            "Data Analyst": [
                {
                    "title": "Sales Performance Dashboard",
                    "description": "Built interactive Power BI dashboard to analyze monthly sales trends and KPIs."
                },
                {
                    "title": "Customer Segmentation Analysis",
                    "description": "Performed clustering analysis using Python to identify customer groups."
                }
            ],

            "Machine Learning Engineer": [
                {
                    "title": "Predictive Maintenance Model",
                    "description": "Developed ML model using Scikit-learn to predict equipment failures."
                },
                {
                    "title": "Spam Detection System",
                    "description": "Built NLP-based spam classifier using Logistic Regression."
                }
            ],

            "Data Scientist": [
                {
                    "title": "Churn Prediction Model",
                    "description": "Implemented predictive model to forecast customer churn."
                },
                {
                    "title": "A/B Testing Framework",
                    "description": "Designed statistical testing framework for product experiments."
                }
            ],

            "Backend Developer": [
                {
                    "title": "REST API System",
                    "description": "Built scalable REST APIs using FastAPI and SQLAlchemy."
                },
                {
                    "title": "Authentication System",
                    "description": "Implemented JWT-based user authentication and authorization."
                }
            ],

            "AI Engineer": [
                {
                    "title": "Image Classification Model",
                    "description": "Trained CNN model for multi-class image classification."
                },
                {
                    "title": "Chatbot using NLP",
                    "description": "Developed conversational AI chatbot using Transformers."
                }
            ],

            "Business Intelligence Analyst": [
                {
                    "title": "Executive KPI Dashboard",
                    "description": "Designed BI dashboards to track business metrics."
                },
                {
                    "title": "Revenue Trend Analysis",
                    "description": "Analyzed revenue patterns to support strategic decisions."
                }
            ],

            "Full Stack Developer": [
                {
                    "title": "Portfolio Website",
                    "description": "Developed full-stack portfolio using FastAPI and Bootstrap."
                },
                {
                    "title": "E-commerce Platform",
                    "description": "Built dynamic shopping platform with backend API integration."
                }
            ],

            "Data Engineer": [
                {
                    "title": "ETL Pipeline System",
                    "description": "Created automated ETL pipeline for large-scale data processing."
                },
                {
                    "title": "Data Warehouse Setup",
                    "description": "Designed data warehouse schema for analytics reporting."
                }
            ],

            "NLP Engineer": [
                {
                    "title": "Sentiment Analysis Model",
                    "description": "Built NLP model for social media sentiment classification."
                },
                {
                    "title": "Text Summarization Tool",
                    "description": "Developed extractive summarization system using Transformers."
                }
            ],

            "Cloud Engineer": [
                {
                    "title": "Cloud Deployment Pipeline",
                    "description": "Implemented CI/CD pipeline for AWS deployment."
                },
                {
                    "title": "Dockerized Application",
                    "description": "Containerized microservices using Docker and Kubernetes."
                }
            ]
        }

        return projects_data.get(role, [])