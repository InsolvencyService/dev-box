Feature: summary details

    Background:
        Given the IP has provided the employee details
            | NAME                               | VALUE      |
            | employee_national_insurance_number | AB111111C  |
            | employee_date_of_birth             | 01/01/1900 |
            | employee_title                     | Mr         |
            | employee_forenames                 | John       |
            | employee_surname                   | Smith      |
            | ip_number                          | 0000       |
            | employer_name                      | Widgets Co |
            | employee_basic_weekly_pay          | 550        |
            | employee_owed_wages_from           | 05/01/2012 |
            | employee_owed_wages_to             | 02/02/2012 |
            | employee_owed_wages_in_arrears     | 1550       |

    @nuke_db
    Scenario: the claimant has provided wages details that are discrepent
        Given the claimant is matched to the employee details
         When the claimant enters the valid wage details
            | NAME                     | VALUE  |
            | frequency_of_payment     | Week   |
            | gross_rate_of_pay        | 600    |
            | frequency_of_work        | Day    |
            | number_of_hours_worked   | 12     |
            | bonus_or_commission      | No     |
            | normal_days_of_work      | 5      |
            | overtime                 | Yes    |
           And the claimant views the summary page
         Then the page should include "Your Insolvency Practitioner has suggested"

    @nuke_db
    Scenario: the claimant has provided discrepant wages owed details
        Given the claimant is matched to the employee details
          And a claimant with the unpaid wage details
            | DETAILS             | VALUE      |
            | owed                | Yes        |
            | wage_owed_from      | 01/01/2012 |
            | wage_owed_to        | 02/02/2012 |
            | number_of_days_owed | 20         |
            | gross_amount_owed   | 2000.00    |
         When the claimant goes to /claim-redundancy-payment/wages-owed-details/
          And enters the unpaid wages details
          And the claimant views the summary page
         Then the page should include "The Insolvency Practitioner has suggested 05/01/2012 to 02/02/2012. Your payment will be calculated using the shorter period of 05/01/2012 to 02/02/2012"



