# ride-my-way-api
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/meshack-mbuvi/ride-my-way-api.svg?branch=develop)](https://travis-ci.org/meshack-mbuvi/ride-my-way-api) [![Coverage Status](https://coveralls.io/repos/github/meshack-mbuvi/ride-my-way-api/badge.svg?branch=develop)](https://coveralls.io/github/meshack-mbuvi/ride-my-way-api?branch=develop)

Ride-my-way App is a carpooling application that provides drivers with the ability to create ride offers and passengers to join the ride offers.

# Api endpoints:

| Endpoint | Description |
| --- | --- |
| POST /auth/signup | Register new user
| POST /auth/login | Login the user using this endpoint
| POST /auth/login | Reset user password
| POST /api/v1//users/rides | Add a new ride offer
| GET /api/v1/rides | retrieve all rides
| GET /api/v1/rides/{ride_id} | retrieve a single ride offer
| POST /api/v1/rides/{ride_id}/requests | Request to join a ride offer
| GET /users/rides/<rideId>/requests | Fetch all ride requests
| PUT /users/rides/<rideId>/requests/<requestId> | Accept/Reject a ride request



# Getting started
The following is a guidelines to get started with this **API**

# Prerequisites
* Install [git](https://gist.github.com/derhuerst/1b15ff4652a867391f03) if it is not installed in your machine.
* Using your terminal run the following commands:
    ```
    - cd path/to/directory-of-your-choice
    - git clone https://github.com/meshack-mbuvi/ride-my-way-api.git
	 - If you do not have [virtual environment](https://virtualenv.pypa.io/en/stable/installation/), install one in your system.
   - cd to ride-my-way-api and execute the following commands:
        
        - $ virtualenv venv 
        - $ source venv/bin/activate
        - $ pip install -r requirements.txt
        
   - To run tests, do:
   
        - $ nosetests
   
   - Then run the app by executing:
        - $ python run.py
        
   - Install and open [Postman](https://www.getpostman.com/) to experiment with the given endpoints.
   - Point to `http://your-server/ride-my-way-api` from postman.
    ```

* Open your favourite browser and point it to ` http://your-server/ride-my-way-api/ ` to experiment with the app.

# Contributing
If you want to contribute to this project:

    * Fork the API!
    * Clone it to your local machine
    * Create your feature branch: ` git checkout -b my-new-feature`
    * Commit your changes: ` git commit -am 'Add some feature' `
    * Push to the branch: ` git push origin my-new-feature `
    * Submit a pull request :D

# Project Owner
   [Andela Kenya](https://www.andela.com/about-us/)

# Software Developer
   [Meshack Mbuvi](https://www.github.com/meshack-mbuvi)



