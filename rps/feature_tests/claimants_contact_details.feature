Feature: claimants contact details

    Scenario: capturing claimants contact details so that they can be contacted by RPS
        Given the app is running
         When we visit /claim-redundancy-payment/personal-details/
         Then the page should have title "Claimant Contact Details"
          And the page should have an input field called "forenames" labeled "First name(s)"
          And the page should have an input field called "surname" labeled "Last name"
          And the page should have an input field called "title" labeled "Title"
          And the page should have an input field called "other" labeled "Other"
          And the page should have an input field called "building_number" labeled "Building Number"
          And the page should have an input field called "street" labeled "Street"
          And the page should have an input field called "district" labeled "District"
          And the page should have an input field called "town_or_city" labeled "Town or City"
          And the page should have an input field called "county" labeled "County"
          And the page should have an input field called "postcode" labeled "Post Code"
          And the page should have an input field called "email" labeled "Email Address"
          And the page should have an input field called "telephone_number" labeled "Telephone Number"
          And the page should have an input field called "nino" labeled "National Insurance Number"
          #TODO: Correct the DOB test when we know what it looks like
          #And the page should have an input field called "date_of_birth" labeled "Date Of Birth"

    Scenario: filling in the contact details form with a missing information
        Given a claimant with the personal details
            | DETAILS           | VALUE             |
            | title             | Mr                |
            | surname           | Duck              |
            | building_number   | 1                 |
            | street            | street name       |
         When the claimant goes to /claim-redundancy-payment/personal-details/
          And enters their details
         Then the claimant should stay on /claimant-contact-details/ with title "Claimant Contact Details"

    Scenario: filling in the contact details from with valid data
        Given a claimant with the personal details
            | DETAILS             | VALUE           |
            | title               | Mr              |
            | forenames           | Bill            |
            | surname             | Bailey          |
            | nino                | ab123456c       |
            | date_of_birth-day   | 12              |
            | date_of_birth-month | 7               |
            | date_of_birth-year  | 1999            |
            | building_number     | 1               |
            | street              | Cannon Street   |
            | district            | Birmingham      |
            | town_or_city        | Birmingham      |
            | county              | West Midlands   |
            | postcode            | W78 9AT         |
            | email               | bill@bailey.com |
            | telephone_number    | 00000000        |
         When the claimant goes to /claim-redundancy-payment/personal-details/
          And enters their details
         Then the claimant should be redirected
          #sent to /claim-redundancy-payment/call-your-ip/
