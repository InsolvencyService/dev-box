@wip
Feature: uploading information about an employer who has become redundant

    Scenario: upload details of a company which has become insolvent
        Given the employer information
            | FIELD_NAME                            | VALUE                             | 
            | company_name                          | Self Pres 12#                     |
            | company_number                        | 98998987                          |
            | nature_of_business                    | Stealing gold from Italian banks  |
            | date_of_insolvency                    | 01/05/2013                        |
            | type_of_insolvency                    | Compulsory Liquidation (WUO)      |
            | insolvency_practitioner_name          | Tywin Lannster                    |
            | insolvency_practitioner_registration  | 9888                              |
            | insolvency_practitioner_firm          | House Lannister of Caterley Rock  |
            | address_line_1                        | 269a                              |
            | address_line_2                        | Winterfell                        |
            | address_line_3                        | Summerhasdied St                  |
            | town_or_city                          | Birmingham                        |
            | postcode                              | B4 6FD                            |
            | country                               | England                           |
            | email_address                         | tywin.lannister@hotmail.co.uk     |
            | telephone_number                      | 07537345763                       |
         When the insolvency practitioner submits the employer information
         Then the information should be submitted to CHAMP

    Scenario: upload details of a company which has become insolvent
        Given the employer information
            | FIELD_NAME                            | VALUE                             | 
            | company_name                          | *MISSING*                         |
            | company_number                        | 98998987                          |
            | nature_of_bussiness                   | *MISSING*                         |
            | date_of_insolvency                    | 01/05/2013                        |
            | type_of_insolvency                    | Compulsory Liquidation (WUO)      |
            | insolvency_practitioner_name          | Tywin Lannster                    |
            | insolvency_practitioner_registration  | 9888                              |
            | insolvency_practitioner_firm          | House Lannister of Caterley Rock  |
            | address_line_1                        | 269a                              |
            | address_line_2                        | Winterfell                        |
            | address_line_3                        | Summerhasdied St                  |
            | town_or_city                          | Birmingham                        |
            | postcode                              | B4 6FD                            |
            | country                               | England                           |
            | email_address                         | tywin.lannister@hotmail.co.uk     |
            | telephone_number                      | 07537345763                       |
         When the insolvency practitioner submits the employer information
         Then the form should display the error message "Name of Employer mandatory fields has not been completed"
          And the form should display the error message "Nature of Bussiness mandatory fields has not been completed"

    Scenario: upload details of a company which has become insolvent
        Given the employer information
            | FIELD_NAME                            | VALUE                             | 
            | company_name                          | Game of Thrones                   |
            | company_number                        | 98998987                          |
            | nature_of_bussiness                   | Butchering people for power       |
            | date_of_insolvency                    | 01/05/2013                        |
            | type_of_insolvency                    | Compulsory Liquidation (WUO)      |
            | insolvency_practitioner_name          | Tywin Lannster                    |
            | insolvency_practitioner_registration  | IP                                |
            | insolvency_practitioner_firm          | House Lannister of Caterley Rock  |
            | address_line_1                        | 269a                              |
            | address_line_2                        | Winterfell                        |
            | address_line_3                        | Summerhasdied St                  |
            | town_or_city                          | Birmingham                        |
            | postcode                              | B4 6FD                            |
            | country                               | England                           |
            | email_address                         | tywin.lannister@hotmail.co.uk     |
            | telephone_number                      | 07537345763                       |
         When the insolvency practitioner submits the employer information
         Then the form should display the error message "IP Registration Number contains invalid data"

