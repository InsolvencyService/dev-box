# Story: discrepancies for wages details
#
# As a: claimant
# I want: to see discrepancies between details I provide and details my IP provides
# So that: I understand the claim I'm making and can resolve discrepancies before I submit

@arrears
Feature: displaying discrepencies to the claimant

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
            | employee_owed_wages_from           | 01/01/2010 |
            | employee_owed_wages_to             | 01/01/2013 |
            | employee_owed_wages_in_arrears     | 5000       |

    @nuke_db
    Scenario: the claimant provides wages details that are discrepent
        Given the claimant is matched to the employee details
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
          But not see a discrepancy on frequency of work

    @nuke_db
    Scenario: the claimant provides wages details that are not discrepent
        Given the claimant is matched to the employee details
         When the claimant enters the valid wage details
            | NAME                     | VALUE  |
            | frequency_of_payment     | Week   | 
            | gross_rate_of_pay        | 550    |
            | frequency_of_work        | Day    |
            | number_of_hours_worked   | 12     |
            | bonus_or_commission      | No     |
            | overtime                 | Yes    |
            | normal_days_of_work      | 5      |
         Then the claimant should see the next page of the form

    @nuke_db
    Scenario: the claimant provides arrears of pay that are discrepent
        Given the claimant is matched to the employee details
         When the claimant enters the valid arrears of pay details
            | NAME                     | VALUE      |
            | owed                     | Yes        |
            | wage_owed_from           | 01/01/2010 |
            | wage_owed_to             | 01/01/2013 |
            | number_of_days_owed      | 1          |
            | gross_amount_owed        | 999        |
         Then the claimant should see a discrepancy on wage owed in arrears


