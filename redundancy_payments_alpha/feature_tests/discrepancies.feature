Feature: displaying discrepancies to the claimant

    Scenario: Claimant provides wages details that are discrepant
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
          And the claimant is matched to the employee details
         When the claimant enters the valid wage details
            | NAME                     | VALUE  |
            | frequency_of_payment     | Week   | 
            | gross_rate_of_pay        | 600    |
            | frequency_of_work        | Day    |
            | number_of_hours_worked   | 12     |
            | bonus_or_commission      | No     |
            | overtime                 | Yes    |
            | normal_days_of_work      | 5      |
        Then the claimant should see a discrepancy on gross rate of pay
         And not see a discrepancy on frequency of work

