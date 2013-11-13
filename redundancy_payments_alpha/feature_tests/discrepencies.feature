Feature: displaying discrepencies to the claimant

    Scenario: Claimant provides wages details that are discrepent
        Given the IP has provided the employee details
            | NAME                     | VALUE      |
            | nino                     | AB111111C  |
            | date_of_birth            | 01/01/1900 |
            | title                    | Mr         |
            | forenames                | John       |
            | surname                  | Smith      |
            | ip_number                | 0000       |
            | employer_name            | Widgets Co |
            | frequency_of_payment     | Month      | 
            | gross_rate_of_pay        | 25000      |
            | frequency_of_work        | Day        |
            | number_of_hours_worked   | 12         |
            | bonus_or_commission      | 0          |
            | overtime                 | 0          |
            | normal_days_of_work      | 5          |
          And the claimant is matched to the employee details
         When the claimant enters the valid wage details
            | NAME                     | VALUE  |
            | frequency_of_payment     | Month  | 
            | gross_rate_of_pay        | 26000  |
            | frequency_of_work        | Day    |
            | number_of_hours_worked   | 12     |
            | bonus_or_commission      | No     |
            | overtime                 | Yes    |
            | normal_days_of_work      | 5      |
        Then the claimant should see a discrepancy on gross rate of pay

