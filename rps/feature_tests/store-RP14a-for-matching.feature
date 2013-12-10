Feature: Employee Information
    Scenario: Store RP14a in database to allow matching
        Given an IP entering the employee details
            | DETAILS                             | VALUE                 |
            | job_title                           | Guardian of the North |
            | employer_name                       | Widgets Co.           |
            | employee_title                      | Other                 |
            | employee_title_other                | Doctor                |
            | employee_forenames                  | J                     |
            | employee_surname                    | Smith                 |
            | employee_national_insurance_class   | z                     |
            | employee_national_insurance_number  | ab123456              |
            | employee_date_of_birth              | 01/01/1940            |
            | employee_start_date                 | 01/01/1980            |
            | employee_date_of_notice             | 01/01/1990            |
            | employee_end_date                   | 05/01/1990            |
            | employee_basic_weekly_pay           | 600                   |
            | employee_weekly_pay_day             | monday                |
            | employee_owed_wages_from            | 01/12/1989            |
            | employee_owed_wages_to              | 05/01/1990            |
            | employee_owed_wages_in_arrears      | 1200.50               |
            | employee_owed_wages_in_arrears_type | wages                 |
            | employee_holiday_year_start_date    | 01/01/1990            |
            | employee_holiday_owed               | 5.5                   |
            | employee_unpaid_holiday_from        | 01/01/1990            |
            | employee_unpaid_holiday_to          | 01/01/1990            |
        When the IP goes to /create-employee-record/employee-details/
        And enters the employee details
        Then the IP should be sent to /create-employee-record/employee-added/
        And the data base should contain an employee


