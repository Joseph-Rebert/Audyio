# Audyio

Audyio is a full-stack text-to-speech application that lets users convert written content into audio using AWS-powered speech synthesis. The project was built to provide a simple, affordable way to turn readings, notes, and other text into listenable audio.

## Features

* Convert text into realistic speech using **Amazon Polly**
* User authentication and account management with **Amazon Cognito**
* Subscription-based access using the **Stripe API**
* Backend deployment with **AWS Elastic Beanstalk**
* PostgreSQL database for storing user and application data
* Full-stack architecture with secure backend processing
* Cloud-hosted infrastructure designed for scalability

## Tech Stack

**Frontend**

* HTML
* CSS
* JavaScript

**Backend**

* Python
* Flask

**Cloud / AWS**

* AWS Elastic Beanstalk
* Amazon Cognito
* Amazon Polly
* AWS Route 53

**Database**

* PostgreSQL

**Payments**

* Stripe API

**Version Control**

* Git
* GitHub

## Project Overview

Audyio allows users to paste text into the application and generate speech audio through Amazon Polly. The app includes user authentication through Amazon Cognito and supports paid subscription tiers through Stripe. User and application data are stored with PostgreSQL, while the backend is deployed using AWS Elastic Beanstalk.

This project helped me gain experience with cloud deployment, payment integration, authentication, database design, and building a real full-stack product.

## Why I Built It

I built Audyio because I wanted a simple way to listen to assigned readings for school while commuting or working. Many existing text-to-speech tools were either too expensive or included more features than I needed, so I decided to build a simpler version focused on practical use.

## What I Learned

* Building and deploying a full-stack application
* Working with AWS services in a real project
* Integrating Stripe payments and subscription logic
* Managing users with Cognito authentication
* Connecting a Flask backend to a PostgreSQL database
* Designing software with scalability and real users in mind

## Future Improvements

* Add more voice customization options
* Improve the user dashboard
* Add saved audio history
* Support file uploads for PDFs or documents
* Add usage tracking by subscription tier
* Improve frontend design and responsiveness

## Installation

Clone the repository:

```bash
git clone https://github.com/Joseph-Rebert/audyio.git
cd audyio
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your environment variables:

```env
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region

STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLIC_KEY=your_stripe_public_key

DATABASE_URL=your_postgresql_database_url

COGNITO_USER_POOL_ID=your_cognito_user_pool_id
COGNITO_CLIENT_ID=your_cognito_client_id
```

Run the application:

```bash
python app.py
```

## Status

This project is currently in development.

## Author

**Joseph Rebert**

* GitHub: [Joseph Rebert](https://github.com/Joseph-Rebert)
* LinkedIn: https://www.linkedin.com/in/joseph-rebert-9243192b3/
* Portfolio: https://joseph-rebert.github.io/Portfolio-Website/
