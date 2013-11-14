Feature: Matching a claimant's personal details to an employee record

    Scenario: Claimant provides details which are matched to an employee record
        Given an employee with the nino AB111111C
        And a claimant with the personal details
            | DETAILS           | VALUE             |
            | forenames         | Donald            |
            | surname           | Duck              |
            | title             | Mr                |
            | building_number   | 1                 |
            | street            | street name       |
            | district          | some district     |
            | town_or_city      | Duckburg          |
            | county            | foobar            |
            | postcode          | a1 4lp            |
            | email             | duck@burg.com     |
            | telephone_number  | 00000 123456      |
            | nino              | AB111111C         |
            | date_of_birth     | 01/01/1900        |
         When the claimant goes to /claim-redundancy-payment/personal-details/
          And enters their details
         Then they are shown their employee record

    Scenario: Claimant provides details which cannot be matched to an employee record
        Given a claimant with the personal details
            | DETAILS           | VALUE             |
            | forenames         | Donald            |
            | surname           | Duck              |
            | title             | Mr                |
            | building_number   | 1                 |
            | street            | street name       |
            | district          | some district     |
            | town_or_city      | Duckburg          |
            | county            | foobar            |
            | postcode          | a1 4lp            |
            | email             | duck@burg.com     |
            | telephone_number  | 00000 123456      |
            | nino              | AB222222C         |
            | date_of_birth     | 01/01/1900        |
         When the claimant goes to /claim-redundancy-payment/personal-details/
          And enters their details
         Then they are shown a message telling them to contact their IP
