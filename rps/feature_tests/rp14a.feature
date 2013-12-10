Feature: rp14a form

    Scenario: adding rp14a form details to data store
        When we add a dictionary containing sample rp14a details
        Then the data store should contain an employee

    Scenario: capturing claimants HR records so that I can provide corroborating evidence to the claimant
     Given the IP app is running
      When we visit /create-employee-record/employee-details/
      Then the page should have title "Employee Information from Insolvency Practitioner"
       And the page should have an input field called "employer_name" labeled "Employer Name"
       And the page should have an input field called "employee_title" labeled "Title"
       And the page should have an input field called "employee_forenames" labeled "Forenames"
       And the page should have an input field called "employee_surname" labeled "Surname"
       And the page should have an input field called "employee_date_of_birth" labeled "Date of Birth"
       And the page should have an input field called "employee_national_insurance_number" labeled "National Insurance Number"
       And the page should have an input field called "employee_national_insurance_class" labeled "NI Class"
       And the page should have an input field called "employee_start_date" labeled "Employment Start Date"
       And the page should have an input field called "employee_date_of_notice" labeled "Date Notice Given"
       And the page should have an input field called "employee_end_date" labeled "Employment End Date"
       And the page should have an input field called "employee_basic_weekly_pay" labeled "Basic Weekly Pay"
       And the page should have an input field called "employee_weekly_pay_day" labeled "If paid weekly, on what day of the week?"
       And the page should have section titled "Periods of arrears for which pay is owed to this employee"
       And the page should have an input field called "employee_owed_wages_from" labeled "Period 1 From"
       And the page should have an input field called "employee_owed_wages_to" labeled "Period 1 To"
       And the page should have an input field called "employee_owed_wages_in_arrears" labeled "Arrears of pay amount"
       And the page should have an input field called "employee_owed_wages_in_arrears_type" labeled "Arrears of pay type"
       And the page should have section titled "Holiday pay owed to this employee"
       And the page should have an input field called "employee_holiday_year_start_date" labeled "Holiday Year Start Date"
       And the page should have an input field called "employee_holiday_owed" labeled "Total number of days holiday owed"
       And the page should have section titled "Holiday taken and not paid"
       And the page should have an input field called "employee_unpaid_holiday_from" labeled "Unpaid holiday From"
       And the page should have an input field called "employee_unpaid_holiday_to" labeled "Unpaid holiday To"
