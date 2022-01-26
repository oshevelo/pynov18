from django.core.exceptions import ValidationError

# number_example = '+380939399996'  # - VALID


def validate_phone(number):
    operators_list = ['039', '050', '063', '066', '067', '068', '073', '091',
                      '092', '093', '094', '095', '096', '097', '098', '099']
    #  first check -> length & integers
    if len(number) != 13:
        raise ValidationError(f'{number} is not a correct phone number'
                              f' LengthError')

    if not str.isdigit(number[1:]):
        raise ValidationError(f'{number} is not a correct phone number'
                              f'NumeralError, all characters should be numbers')

    #  second check -> country code
    if number[0:3] != '+38':
        raise ValidationError(f'{number} is not a correct phone number'
                              f' CountryCodeError ({number[0:3]})')

    #  third check -> mobile operators
    if number[3:6] not in operators_list:
        raise ValidationError(f'{number} is not a correct phone number'
                              f' OperatorCodeError ({number[3:6]})')