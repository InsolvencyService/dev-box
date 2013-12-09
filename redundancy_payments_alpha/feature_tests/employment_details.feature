Feature: employment details

    Scenario: capturing employment details so that RPS can verify these details
        Given the app is running
         When we visit /claim-redundancy-payment/employment-details/
         Then the page should have title "Employment Details"
          And the page should have an input field called "job_title" labeled "Job Title"
          And the page should have an input field called "type_of_worker" labeled "What type of worker are you?"
          And the page should have an input field called "start_date" labeled "When did you start working for this employer?"
          And the page should have an input field called "end_date" labeled "When did your employment end?"

    Scenario: filling in the contact details form
        Given a claimant with the employment details
            | DETAILS            | VALUE                 |
            | job_title          | Guardian of the North |
            | type_of_worker     | employed              |
            | start_date-day     | 1                     |
            | start_date-month   | 4                     |
            | start_date-year    | 1999                  |
            | end_date-day       | 1                     |
            | end_date-month     | 10                    |
            | end_date-year      | 2013                  |
          When the claimant goes to /claim-redundancy-payment/employment-details/
          And enters the employment details
         Then the claimant should be sent to /claim-redundancy-payment/wage-details/

    Scenario: filling in the contact details form with a missing information
        Given a claimant with the employment details
            | DETAILS            | VALUE                 |
            | job_title          | Guardian of the North |
            | type_of_worker     | employed              |
         When the claimant goes to /claim-redundancy-payment/personal-details/
          And enters the employment details
         Then the claimant should stay on /employment-details/ with title "Employment Details"

    Scenario: filling employment details with a end date earlier than the start date
        Given a claimant with the employment details
            | DETAILS            | VALUE                 |
            | job_title          | Guardian of the North |
            | type_of_worker     | employed              |
            | start_date-day     | 1                     |
            | start_date-month   | 4                     |
            | start_date-year    | 2013                  |
            | end_date-day       | 1                     |
            | end_date-month     | 10                    |
            | end_date-year      | 2012                  |
        When the claimant goes to /claim-redundancy-payment/employment-details/
         And enters the employment details
        Then the claimant should stay on /employment-details/ with title "Employment Details"
         And the page should include "The end date cannot be before the start date"

    Scenario: filling employment details with multiple errors
        Given a claimant with the employment details
            | DETAILS            | VALUE                 |
            | job_title          | Guardian of the North |
            | start_date-day     | 1                     |
            | start_date-month   | 4                     |
            | start_date-year    | 2013                  |
            | end_date-day       | 13                    |
            | end_date-month     | 1                     |
            | end_date-year      | 2012                  |
        When the claimant goes to /claim-redundancy-payment/employment-details/
         And enters the employment details
        Then the claimant should stay on /employment-details/ with title "Employment Details"
         And the page should include "The end date cannot be before the start date"
