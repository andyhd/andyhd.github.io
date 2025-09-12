Date: 2021-03-07 19:37
Status: draft
Title: Building a microservice with Python and Zappa
Friendly-Date: a Sunday evening before dinner


# Achievements as a Service

Trying to do as little as possible.

## The Ingredients

- Flask
- Zappa
- AWS RDS
- SQLAlchemy

## The Plan

Build a webservice with Flask, hosted in AWS via Zappa, backed by an AWS RDS database,
accessed via SQLAlchemy.

For a first draft, the webservice will have a simple API:

- Add a type of achievement.
  For example, we might add "Logged in 10 times" as a type of achievement.
  
- Record progress towards an achievement.
  For example, logging in to our client app might record progress towards the "Logged in
  10 times" achievement.
