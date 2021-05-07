"""Enums for the ratings_central app."""
from django.utils.translation import gettext_lazy as _

from choices import IntegerChoices, TextChoices


class Gender(TextChoices):
    """Gender choices offered by ratings central."""

    MALE = "M", _("Male")
    FEMALE = "F", _("Female")


class ClubStatus(TextChoices):
    """Club statuses offered by ratings central."""

    ACTIVE = "Active", _("Active")
    INACTIVE = "Inactive", _("Inactive")


class Sport(IntegerChoices):
    """Sport choices offered by ratings central."""

    TABLE_TENNIS = 1, _("Table Tennis")
    HARDBAT = 3, _("Hardbat Table Tennis")
    SANDPAPER = 4, _("Sandpaper Table Tennis")


class Country(TextChoices):
    """Country choices offered by ratings central."""

    AFG = "AFG", _("Afghanistan")
    ALB = "ALB", _("Albania")
    ALG = "ALG", _("Algeria")
    ASA = "ASA", _("American Samoa")
    AND = "AND", _("Andorra")
    ANG = "ANG", _("Angola")
    ANT = "ANT", _("Antigua and Barbuda")
    ARG = "ARG", _("Argentina")
    ARM = "ARM", _("Armenia")
    ARU = "ARU", _("Aruba")
    AUS = "AUS", _("Australia")
    AUT = "AUT", _("Austria")
    AZE = "AZE", _("Azerbaijan")
    BAH = "BAH", _("Bahamas")
    BRN = "BRN", _("Bahrain")
    BAN = "BAN", _("Bangladesh")
    BAR = "BAR", _("Barbados")
    BLR = "BLR", _("Belarus")
    BEL = "BEL", _("Belgium")
    BIZ = "BIZ", _("Belize")
    BEN = "BEN", _("Benin")
    BER = "BER", _("Bermuda")
    BHU = "BHU", _("Bhutan")
    BOL = "BOL", _("Bolivia")
    BIH = "BIH", _("Bosnia and Herzegovina")
    BOT = "BOT", _("Botswana")
    BRA = "BRA", _("Brazil")
    IVB = "IVB", _("British Virgin Islands")
    BRU = "BRU", _("Brunei")
    BUL = "BUL", _("Bulgaria")
    BUR = "BUR", _("Burkina Faso")
    BDI = "BDI", _("Burundi")
    CAM = "CAM", _("Cambodia")
    CMR = "CMR", _("Cameroon")
    CAN = "CAN", _("Canada")
    CPV = "CPV", _("Cape Verde")
    CAY = "CAY", _("Cayman Islands")
    CAF = "CAF", _("Central African Republic")
    CHA = "CHA", _("Chad")
    CHI = "CHI", _("Chile")
    CHN = "CHN", _("China")
    TPE = "TPE", _("Chinese Taipei")
    COL = "COL", _("Colombia")
    COM = "COM", _("Comoros")
    COK = "COK", _("Cook Islands")
    CRC = "CRC", _("Costa Rica")
    CRO = "CRO", _("Croatia")
    CUB = "CUB", _("Cuba")
    CUW = "CUW", _("Curaçao")
    CYP = "CYP", _("Cyprus")
    CZE = "CZE", _("Czech Republic")
    TCH = "TCH", _("Czechoslovakia")
    COD = "COD", _("Democratic Republic of the Congo")
    DEN = "DEN", _("Denmark")
    DJI = "DJI", _("Djibouti")
    DMA = "DMA", _("Dominica")
    DOM = "DOM", _("Dominican Republic")
    TLS = "TLS", _("East Timor")
    ECU = "ECU", _("Ecuador")
    EGY = "EGY", _("Egypt")
    ESA = "ESA", _("El Salvador")
    ENG = "ENG", _("England")
    GEQ = "GEQ", _("Equatorial Guinea")
    ERI = "ERI", _("Eritrea")
    EST = "EST", _("Estonia")
    SWZ = "SWZ", _("Eswatini")
    ETH = "ETH", _("Ethiopia")
    FLK = "FLK", _("Falkland Islands")
    FRO = "FRO", _("Faroe Islands")
    FSM = "FSM", _("Federated States of Micronesia")
    FIJ = "FIJ", _("Fiji")
    FIN = "FIN", _("Finland")
    FRA = "FRA", _("France")
    GAB = "GAB", _("Gabon")
    GEO = "GEO", _("Georgia")
    GER = "GER", _("Germany")
    GDR = "GDR", _("Germany D.R.")
    FRG = "FRG", _("Germany F.R.")
    GHA = "GHA", _("Ghana")
    GIB = "GIB", _("Gibraltar")
    GBR = "GBR", _("Great Britain")
    GRE = "GRE", _("Greece")
    GRN = "GRN", _("Grenada")
    GUM = "GUM", _("Guam")
    GUA = "GUA", _("Guatemala")
    GGY = "GGY", _("Guernsey")
    GUI = "GUI", _("Guinea")
    GBS = "GBS", _("Guinea-Bissau")
    GUY = "GUY", _("Guyana")
    HAI = "HAI", _("Haiti")
    HON = "HON", _("Honduras")
    HKG = "HKG", _("Hong Kong")
    HUN = "HUN", _("Hungary")
    ISL = "ISL", _("Iceland")
    IND = "IND", _("India")
    INA = "INA", _("Indonesia")
    IRI = "IRI", _("Iran")
    IRQ = "IRQ", _("Iraq")
    IRL = "IRL", _("Ireland")
    IMN = "IMN", _("Isle of Man")
    ISR = "ISR", _("Israel")
    ITA = "ITA", _("Italy")
    CIV = "CIV", _("Ivory Coast")
    JAM = "JAM", _("Jamaica")
    JPN = "JPN", _("Japan")
    JEY = "JEY", _("Jersey")
    JOR = "JOR", _("Jordan")
    KAZ = "KAZ", _("Kazakhstan")
    KEN = "KEN", _("Kenya")
    KIR = "KIR", _("Kiribati")
    KOS = "KOS", _("Kosovo")
    KUW = "KUW", _("Kuwait")
    KGZ = "KGZ", _("Kyrgyzstan")
    LAO = "LAO", _("Laos")
    LAT = "LAT", _("Latvia")
    LBN = "LBN", _("Lebanon")
    LES = "LES", _("Lesotho")
    LBR = "LBR", _("Liberia")
    LBA = "LBA", _("Libya")
    LIE = "LIE", _("Liechtenstein")
    LTU = "LTU", _("Lithuania")
    LUX = "LUX", _("Luxembourg")
    MAC = "MAC", _("Macau")
    MAD = "MAD", _("Madagascar")
    MAW = "MAW", _("Malawi")
    MAS = "MAS", _("Malaysia")
    MDV = "MDV", _("Maldives")
    MLI = "MLI", _("Mali")
    MLT = "MLT", _("Malta")
    MHL = "MHL", _("Marshall Islands")
    MTN = "MTN", _("Mauritania")
    MRI = "MRI", _("Mauritius")
    MEX = "MEX", _("Mexico")
    MDA = "MDA", _("Moldova")
    MON = "MON", _("Monaco")
    MGL = "MGL", _("Mongolia")
    MNE = "MNE", _("Montenegro")
    MSR = "MSR", _("Montserrat")
    MAR = "MAR", _("Morocco")
    MOZ = "MOZ", _("Mozambique")
    MYA = "MYA", _("Myanmar")
    NAM = "NAM", _("Namibia")
    NRU = "NRU", _("Nauru")
    NEP = "NEP", _("Nepal")
    NED = "NED", _("Netherlands")
    AHO = "AHO", _("Netherlands Antilles")
    NZL = "NZL", _("New Zealand")
    NCA = "NCA", _("Nicaragua")
    NIG = "NIG", _("Niger")
    NGR = "NGR", _("Nigeria")
    NIU = "NIU", _("Niue")
    NFK = "NFK", _("Norfolk Island")
    PRK = "PRK", _("North Korea")
    MKD = "MKD", _("North Macedonia")
    NIR = "NIR", _("Northern Ireland")
    NOR = "NOR", _("Norway")
    OMA = "OMA", _("Oman")
    PAK = "PAK", _("Pakistan")
    PLW = "PLW", _("Palau")
    PLE = "PLE", _("Palestine")
    PAN = "PAN", _("Panama")
    PNG = "PNG", _("Papua New Guinea")
    PAR = "PAR", _("Paraguay")
    PER = "PER", _("Peru")
    PHI = "PHI", _("Philippines")
    POL = "POL", _("Poland")
    POR = "POR", _("Portugal")
    PUR = "PUR", _("Puerto Rico")
    QAT = "QAT", _("Qatar")
    CGO = "CGO", _("Republic of the Congo")
    ROU = "ROU", _("Romania")
    RUS = "RUS", _("Russia")
    RWA = "RWA", _("Rwanda")
    SKN = "SKN", _("Saint Kitts and Nevis")
    LCA = "LCA", _("Saint Lucia")
    VIN = "VIN", _("Saint Vincent and the Grenadines")
    SAM = "SAM", _("Samoa")
    SMR = "SMR", _("San Marino")
    STP = "STP", _("São Tomé and Príncipe")
    KSA = "KSA", _("Saudi Arabia")
    SCO = "SCO", _("Scotland")
    SEN = "SEN", _("Senegal")
    SRB = "SRB", _("Serbia")
    SCG = "SCG", _("Serbia and Montenegro")
    SEY = "SEY", _("Seychelles")
    SLE = "SLE", _("Sierra Leone")
    SGP = "SGP", _("Singapore")
    SVK = "SVK", _("Slovakia")
    SLO = "SLO", _("Slovenia")
    SOL = "SOL", _("Solomon Islands")
    SOM = "SOM", _("Somalia")
    RSA = "RSA", _("South Africa")
    KOR = "KOR", _("South Korea")
    SSD = "SSD", _("South Sudan")
    ESP = "ESP", _("Spain")
    SRI = "SRI", _("Sri Lanka")
    SUD = "SUD", _("Sudan")
    SUR = "SUR", _("Suriname")
    SWE = "SWE", _("Sweden")
    SUI = "SUI", _("Switzerland")
    SYR = "SYR", _("Syria")
    TJK = "TJK", _("Tajikistan")
    TAN = "TAN", _("Tanzania")
    THA = "THA", _("Thailand")
    GAM = "GAM", _("The Gambia")
    TOG = "TOG", _("Togo")
    TKL = "TKL", _("Tokelau")
    TGA = "TGA", _("Tonga")
    TTO = "TTO", _("Trinidad and Tobago")
    TUN = "TUN", _("Tunisia")
    TUR = "TUR", _("Turkey")
    TKM = "TKM", _("Turkmenistan")
    TCA = "TCA", _("Turks and Caicos")
    TUV = "TUV", _("Tuvalu")
    UGA = "UGA", _("Uganda")
    UKR = "UKR", _("Ukraine")
    UAE = "UAE", _("United Arab Emirates")
    USA = "USA", _("United States")
    URU = "URU", _("Uruguay")
    URS = "URS", _("USSR")
    UZB = "UZB", _("Uzbekistan")
    VAN = "VAN", _("Vanuatu")
    VEN = "VEN", _("Venezuela")
    VIE = "VIE", _("Vietnam")
    ISV = "ISV", _("Virgin Islands")
    WAL = "WAL", _("Wales")
    YEM = "YEM", _("Yemen")
    YUG = "YUG", _("Yugoslavia")
    ZAM = "ZAM", _("Zambia")
    ZIM = "ZIM", _("Zimbabwe")


class NorthAmericaState(TextChoices):
    """North American (USA and CAN) states choices offered by ratings central."""

    # USA
    AL = "AL", _("Alabama")
    AK = "AK", _("Alaska")
    AS = "AS", _("American Samoa")
    AZ = "AZ", _("Arizona")
    AR = "AR", _("Arkansas")
    AE = "AE", _("Armed Forces Europe")
    AP = "AP", _("Armed Forces Pacific")
    AA = "AA", _("Armed Forces the Americas")
    CA = "CA", _("California")
    CO = "CO", _("Colorado")
    CT = "CT", _("Connecticut")
    DE = "DE", _("Delaware")
    DC = "DC", _("District of Columbia")
    FM = "FM", _("Federated States of Micronesia")
    FL = "FL", _("Florida")
    GA = "GA", _("Georgia")
    GU = "GU", _("Guam")
    HI = "HI", _("Hawaii")
    ID = "ID", _("Idaho")
    IL = "IL", _("Illinois")
    IN = "IN", _("Indiana")
    IA = "IA", _("Iowa")
    KS = "KS", _("Kansas")
    KY = "KY", _("Kentucky")
    LA = "LA", _("Louisiana")
    ME = "ME", _("Maine")
    MH = "MH", _("Marshall Islands")
    MD = "MD", _("Maryland")
    MA = "MA", _("Massachusetts")
    MI = "MI", _("Michigan")
    MN = "MN", _("Minnesota")
    MS = "MS", _("Mississippi")
    MO = "MO", _("Missouri")
    MT = "MT", _("Montana")
    NE = "NE", _("Nebraska")
    NV = "NV", _("Nevada")
    NH = "NH", _("New Hampshire")
    NJ = "NJ", _("New Jersey")
    NM = "NM", _("New Mexico")
    NY = "NY", _("New York")
    NC = "NC", _("North Carolina")
    ND = "ND", _("North Dakota")
    MP = "MP", _("Northern Mariana Islands")
    OH = "OH", _("Ohio")
    OK = "OK", _("Oklahoma")
    OR = "OR", _("Oregon")
    PW = "PW", _("Palau")
    PA = "PA", _("Pennsylvania")
    PR = "PR", _("Puerto Rico")
    RI = "RI", _("Rhode Island")
    SC = "SC", _("South Carolina")
    SD = "SD", _("South Dakota")
    TN = "TN", _("Tennessee")
    TX = "TX", _("Texas")
    UT = "UT", _("Utah")
    VT = "VT", _("Vermont")
    VI = "VI", _("Virgin Islands of the U.S.")
    VA = "VA", _("Virginia")
    WA = "WA", _("Washington")
    WV = "WV", _("West Virginia")
    WI = "WI", _("Wisconsin")
    WY = "WY", _("Wyoming")
    # CAN
    AB = "AB", _("Alberta")
    BC = "BC", _("British Columbia")
    MB = "MB", _("Manitoba")
    NB = "NB", _("New Brunswick")
    NL = "NL", _("Newfoundland and Labrador")
    NT = "NT", _("Northwest Territories")
    NS = "NS", _("Nova Scotia")
    NU = "NU", _("Nunavut")
    ON = "ON", _("Ontario")
    PE = "PE", _("Prince Edward Island")
    QC = "QC", _("Quebec")
    SK = "SK", _("Saskatchewan")
    YT = "YT", _("Yukon")