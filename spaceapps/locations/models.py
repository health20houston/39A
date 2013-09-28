from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from projects.models import Project


TIME_ZONE_CHOICES = (
        ('-12.0', '(GMT -12:00) Eniwetok, Kwajalein'),
        ('-11.0', '(GMT -11:00) Midway Island, Samoa'),
        ('-10.0', '(GMT -10:00) Hawaii'),
        ('-9.0', '(GMT -9:00) Alaska'),
        ('-8.0', '(GMT -8:00) Pacific Time (US & Canada)'),
        ('-7.0', '(GMT -7:00) Mountain Time (US & Canada)'),
        ('-6.0', '(GMT -6:00) Central Time (US & Canada), Mexico City'),
        ('-5.0', '(GMT -5:00) Eastern Time (US & Canada), Bogota, Lima'),
        ('-4.0', '(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz'),
        ('-3.5', '(GMT -3:30) Newfoundland'),
        ('-3.0', '(GMT -3:00) Brazil, Buenos Aires, Georgetown'),
        ('-2.0', '(GMT -2:00) Mid-Atlantic'),
        ('-1.0', '(GMT -1:00 hour) Azores, Cape Verde Islands'),
        ('0.0', '(GMT) Western Europe Time, London, Lisbon, Casablanca'),
        ('1.0', '(GMT +1:00 hour) Brussels, Copenhagen, Madrid, Paris'),
        ('2.0', '(GMT +2:00) Kaliningrad, South Africa'),
        ('3.0', '(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg'),
        ('3.5', '(GMT +3:30) Tehran'),
        ('4.0', '(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi'),
        ('4.5', '(GMT +4:30) Kabul'),
        ('5.0', '(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent'),
        ('5.5', '(GMT +5:30) Bombay, Calcutta, Madras, New Delhi'),
        ('5.75', '(GMT +5:45) Kathmandu'),
        ('6.0', '(GMT +6:00) Almaty, Dhaka, Colombo'),
        ('7.0', '(GMT +7:00) Bangkok, Hanoi, Jakarta'),
        ('8.0', '(GMT +8:00) Beijing, Perth, Singapore, Hong Kong'),
        ('9.0', '(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk'),
        ('9.5', '(GMT +9:30) Adelaide, Darwin'),
        ('10.0', '(GMT +10:00) Eastern Australia, Guam, Vladivostok'),
        ('11.0', '(GMT +11:00) Magadan, Solomon Islands, New Caledonia'),
        ('12.0', '(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka')
        )

COUNTRIES = (
        ('AF', _(u'Afghanistan')),
        ('AX', _(u'\xc5land Islands')),
        ('AL', _(u'Albania')),
        ('DZ', _(u'Algeria')),
        ('AS', _(u'American Samoa')),
        ('AD', _(u'Andorra')),
        ('AO', _(u'Angola')),
        ('AI', _(u'Anguilla')),
        ('AQ', _(u'Antarctica')),
        ('AG', _(u'Antigua and Barbuda')),
        ('AR', _(u'Argentina')),
        ('AM', _(u'Armenia')),
        ('AW', _(u'Aruba')),
        ('SH', _(u'Ascension and Tristan Da Cunha Saint Helena')),
        ('AU', _(u'Australia')),
        ('AT', _(u'Austria')),
        ('AZ', _(u'Azerbaijan')),
        ('BS', _(u'Bahamas')),
        ('BH', _(u'Bahrain')),
        ('BD', _(u'Bangladesh')),
        ('BB', _(u'Barbados')),
        ('BY', _(u'Belarus')),
        ('BE', _(u'Belgium')),
        ('BZ', _(u'Belize')),
        ('BJ', _(u'Benin')),
        ('BM', _(u'Bermuda')),
        ('BT', _(u'Bhutan')),
        ('VE', _(u'Bolivarian Republic of Venezuela')),
        ('BO', _(u'Bolivia, Plurinational State of')),
        ('BQ', _(u'Bonaire, Sint Eustatius and Saba')),
        ('BA', _(u'Bosnia and Herzegovina')),
        ('BW', _(u'Botswana')),
        ('BV', _(u'Bouvet Island')),
        ('BR', _(u'Brazil')),
        ('IO', _(u'British Indian Ocean Territory')),
        ('VG', _(u'British Virgin Islands')),
        ('BN', _(u'Brunei Darussalam')),
        ('BG', _(u'Bulgaria')),
        ('BF', _(u'Burkina Faso')),
        ('BI', _(u'Burundi')),
        ('KH', _(u'Cambodia')),
        ('CM', _(u'Cameroon')),
        ('CA', _(u'Canada')),
        ('CV', _(u'Cape Verde')),
        ('KY', _(u'Cayman Islands')),
        ('CF', _(u'Central African Republic')),
        ('TD', _(u'Chad')),
        ('CL', _(u'Chile')),
        ('CN', _(u'China')),
        ('CX', _(u'Christmas Island')),
        ('CC', _(u'Cocos (Keeling) Islands')),
        ('CO', _(u'Colombia')),
        ('KM', _(u'Comoros')),
        ('CG', _(u'Congo')),
        ('CD', _(u'Congo, The Democratic Republic of the')),
        ('CK', _(u'Cook Islands')),
        ('CR', _(u'Costa Rica')),
        ('CI', _(u"C\xf4te D'ivoire")),
        ('HR', _(u'Croatia')),
        ('CU', _(u'Cuba')),
        ('CW', _(u'Cura\xe7ao')),
        ('CY', _(u'Cyprus')),
        ('CZ', _(u'Czech Republic')),
        ('KP', _(u"Democratic People's Republic of Korea")),
        ('DK', _(u'Denmark')),
        ('DJ', _(u'Djibouti')),
        ('DM', _(u'Dominica')),
        ('DO', _(u'Dominican Republic')),
        ('EC', _(u'Ecuador')),
        ('EG', _(u'Egypt')),
        ('SV', _(u'El Salvador')),
        ('GQ', _(u'Equatorial Guinea')),
        ('ER', _(u'Eritrea')),
        ('EE', _(u'Estonia')),
        ('ET', _(u'Ethiopia')),
        ('FK', _(u'Falkland Islands (Malvinas)')),
        ('FO', _(u'Faroe Islands')),
        ('FM', _(u'Federated States of Micronesia')),
        ('FJ', _(u'Fiji')),
        ('FI', _(u'Finland')),
        ('FR', _(u'France')),
        ('GF', _(u'French Guiana')),
        ('PF', _(u'French Polynesia')),
        ('TF', _(u'French Southern Territories')),
        ('GA', _(u'Gabon')),
        ('GM', _(u'Gambia')),
        ('GE', _(u'Georgia')),
        ('DE', _(u'Germany')),
        ('GH', _(u'Ghana')),
        ('GI', _(u'Gibraltar')),
        ('GR', _(u'Greece')),
        ('GL', _(u'Greenland')),
        ('GD', _(u'Grenada')),
        ('GP', _(u'Guadeloupe')),
        ('GU', _(u'Guam')),
        ('GT', _(u'Guatemala')),
        ('GG', _(u'Guernsey')),
        ('GN', _(u'Guinea')),
        ('GW', _(u'Guinea-bissau')),
        ('GY', _(u'Guyana')),
        ('HT', _(u'Haiti')),
        ('HM', _(u'Heard Island and McDonald Islands')),
        ('VA', _(u'Holy See (Vatican City State)')),
        ('HN', _(u'Honduras')),
        ('HK', _(u'Hong Kong')),
        ('HU', _(u'Hungary')),
        ('IS', _(u'Iceland')),
        ('IN', _(u'India')),
        ('ID', _(u'Indonesia')),
        ('IR', _(u'Iran, Islamic Republic of')),
        ('IQ', _(u'Iraq')),
        ('IE', _(u'Ireland')),
        ('IR', _(u'Islamic Republic of Iran')),
        ('IM', _(u'Isle of Man')),
        ('IL', _(u'Israel')),
        ('IT', _(u'Italy')),
        ('JM', _(u'Jamaica')),
        ('JP', _(u'Japan')),
        ('JE', _(u'Jersey')),
        ('JO', _(u'Jordan')),
        ('KZ', _(u'Kazakhstan')),
        ('KE', _(u'Kenya')),
        ('KI', _(u'Kiribati')),
        ('KP', _(u"Korea, Democratic People's Republic of")),
        ('KR', _(u'Korea, Republic of')),
        ('KW', _(u'Kuwait')),
        ('KG', _(u'Kyrgyzstan')),
        ('LA', _(u"Lao People's Democratic Republic")),
        ('LV', _(u'Latvia')),
        ('LB', _(u'Lebanon')),
        ('LS', _(u'Lesotho')),
        ('LR', _(u'Liberia')),
        ('LY', _(u'Libya')),
        ('LI', _(u'Liechtenstein')),
        ('LT', _(u'Lithuania')),
        ('LU', _(u'Luxembourg')),
        ('MO', _(u'Macao')),
        ('MK', _(u'Macedonia, The Former Yugoslav Republic of')),
        ('MG', _(u'Madagascar')),
        ('MW', _(u'Malawi')),
        ('MY', _(u'Malaysia')),
        ('MV', _(u'Maldives')),
        ('ML', _(u'Mali')),
        ('MT', _(u'Malta')),
        ('MH', _(u'Marshall Islands')),
        ('MQ', _(u'Martinique')),
        ('MR', _(u'Mauritania')),
        ('MU', _(u'Mauritius')),
        ('YT', _(u'Mayotte')),
        ('MX', _(u'Mexico')),
        ('FM', _(u'Micronesia, Federated States of')),
        ('MD', _(u'Moldova, Republic of')),
        ('MC', _(u'Monaco')),
        ('MN', _(u'Mongolia')),
        ('ME', _(u'Montenegro')),
        ('MS', _(u'Montserrat')),
        ('MA', _(u'Morocco')),
        ('MZ', _(u'Mozambique')),
        ('MM', _(u'Myanmar')),
        ('NA', _(u'Namibia')),
        ('NR', _(u'Nauru')),
        ('NP', _(u'Nepal')),
        ('NL', _(u'Netherlands')),
        ('NC', _(u'New Caledonia')),
        ('NZ', _(u'New Zealand')),
        ('NI', _(u'Nicaragua')),
        ('NE', _(u'Niger')),
        ('NG', _(u'Nigeria')),
        ('NU', _(u'Niue')),
        ('NF', _(u'Norfolk Island')),
        ('MP', _(u'Northern Mariana Islands')),
        ('NO', _(u'Norway')),
        ('PS', _(u'Occupied Palestinian Territory')),
        ('OM', _(u'Oman')),
        ('PK', _(u'Pakistan')),
        ('PW', _(u'Palau')),
        ('PS', _(u'Palestinian Territory, Occupied')),
        ('PA', _(u'Panama')),
        ('PG', _(u'Papua New Guinea')),
        ('PY', _(u'Paraguay')),
        ('PE', _(u'Peru')),
        ('PH', _(u'Philippines')),
        ('PN', _(u'Pitcairn')),
        ('BO', _(u'Plurinational State of Bolivia')),
        ('PL', _(u'Poland')),
        ('PT', _(u'Portugal')),
        ('TW', _(u'Province of China Taiwan')),
        ('PR', _(u'Puerto Rico')),
        ('QA', _(u'Qatar')),
        ('KR', _(u'Republic of Korea')),
        ('MD', _(u'Republic of Moldova')),
        ('RE', _(u'R\xe9union')),
        ('RO', _(u'Romania')),
        ('RU', _(u'Russian Federation')),
        ('RW', _(u'Rwanda')),
        ('BL', _(u'Saint Barth\xe9lemy')),
        ('SH', _(u'Saint Helena, Ascension and Tristan Da Cunha')),
        ('KN', _(u'Saint Kitts and Nevis')),
        ('LC', _(u'Saint Lucia')),
        ('MF', _(u'Saint Martin (French Part)')),
        ('PM', _(u'Saint Pierre and Miquelon')),
        ('VC', _(u'Saint Vincent and the Grenadines')),
        ('WS', _(u'Samoa')),
        ('SM', _(u'San Marino')),
        ('ST', _(u'Sao Tome and Principe')),
        ('SA', _(u'Saudi Arabia')),
        ('SN', _(u'Senegal')),
        ('RS', _(u'Serbia')),
        ('SC', _(u'Seychelles')),
        ('SL', _(u'Sierra Leone')),
        ('SG', _(u'Singapore')),
        ('BQ', _(u'Sint Eustatius and Saba Bonaire')),
        ('SX', _(u'Sint Maarten (Dutch Part)')),
        ('SK', _(u'Slovakia')),
        ('SI', _(u'Slovenia')),
        ('SB', _(u'Solomon Islands')),
        ('SO', _(u'Somalia')),
        ('ZA', _(u'South Africa')),
        ('GS', _(u'South Georgia and the South Sandwich Islands')),
        ('SS', _(u'South Sudan')),
        ('ES', _(u'Spain')),
        ('LK', _(u'Sri Lanka')),
        ('SD', _(u'Sudan')),
        ('SR', _(u'Suriname')),
        ('SJ', _(u'Svalbard and Jan Mayen')),
        ('SZ', _(u'Swaziland')),
        ('SE', _(u'Sweden')),
        ('CH', _(u'Switzerland')),
        ('SY', _(u'Syrian Arab Republic')),
        ('TW', _(u'Taiwan, Province of China')),
        ('TJ', _(u'Tajikistan')),
        ('TZ', _(u'Tanzania, United Republic of')),
        ('TH', _(u'Thailand')),
        ('CD', _(u'The Democratic Republic of the Congo')),
        ('MK', _(u'The Former Yugoslav Republic of Macedonia')),
        ('TL', _(u'Timor-leste')),
        ('TG', _(u'Togo')),
        ('TK', _(u'Tokelau')),
        ('TO', _(u'Tonga')),
        ('TT', _(u'Trinidad and Tobago')),
        ('TN', _(u'Tunisia')),
        ('TR', _(u'Turkey')),
        ('TM', _(u'Turkmenistan')),
        ('TC', _(u'Turks and Caicos Islands')),
        ('TV', _(u'Tuvalu')),
        ('VI', _(u'U.S. Virgin Islands')),
        ('UG', _(u'Uganda')),
        ('UA', _(u'Ukraine')),
        ('AE', _(u'United Arab Emirates')),
        ('GB', _(u'United Kingdom')),
        ('TZ', _(u'United Republic of Tanzania')),
        ('US', _(u'United States')),
        ('UM', _(u'United States Minor Outlying Islands')),
        ('UY', _(u'Uruguay')),
        ('UZ', _(u'Uzbekistan')),
        ('VU', _(u'Vanuatu')),
        ('VE', _(u'Venezuela, Bolivarian Republic of')),
        ('VN', _(u'Viet Nam')),
        ('VG', _(u'Virgin Islands, British')),
        ('VI', _(u'Virgin Islands, U.S.')),
        ('WF', _(u'Wallis and Futuna')),
        ('EH', _(u'Western Sahara')),
        ('YE', _(u'Yemen')),
        ('ZM', _(u'Zambia')),
        ('ZW', _(u'Zimbabwe')),
        )

CONTINENTS = (
        ('AF', 'Africa'),
        ('AN', 'Antarctica'),
        ('AU', 'Australiasia'),
        ('AS', 'Asia'),
        ('EU', 'Europe'),
        ('NA', 'North America'),
        ('SA', 'South America')
        )

class Location(models.Model):
    """
    Location model for each venue.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()
    description = models.TextField()
    timezone = models.CharField(
        max_length=5, 
        choices=TIME_ZONE_CHOICES, 
        blank=True,
        )
    street = models.CharField(max_length=100, blank=True) 
    street2 = models.CharField(max_length=100, blank=True) 
    city = models.CharField(max_length=32, blank=True, unique=True)
    state = models.CharField(max_length=32, blank=True)
    postal = models.CharField(max_length=32, blank=True) 
    country = models.CharField(max_length=2, choices=COUNTRIES)
    continent = models.CharField(max_length=2, choices=CONTINENTS, blank=True)
    lat = models.FloatField(verbose_name='Latitude')
    lon = models.FloatField(verbose_name='Longitude')
    private = models.BooleanField(
        default=False,
        help_text=('Designate whether this location will be displayed '  
        'publicly.')
        )
    open = models.BooleanField(
        default=True, 
        help_text='Designate whether this location is open for registration.'
        )
    capacity = models.IntegerField(max_length=1000)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True) 
    image = models.ImageField(upload_to="location", blank=True)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = "Locations"

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'locations:detail',
            kwargs={'slug': self.slug}
            )

    def is_full(self):
        """
        Returns whether the location is full.
        """
        from registration.models import Registration
        if self.capacity <= Registration.objects.filter(location=self).count():
            return True 
        else:
            return False

class Sponsor(models.Model):
    """
    Sponsors for locations.
    """
    location = models.ForeignKey(Location)
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="sponsors", blank=True)
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        model = self.__class__
        
        if self.order is None:
            # Append
            try:
                last = model.objects.order_by('-position')[0]
                self.order = last.order + 1
            except IndexError:
                # First row
                self.order = 0
        
        return super(Sponsor, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ('order',)

class Lead(models.Model):
    """
    Which users are leads for a given location.  This imparts administrative 
    privileges to the identified user for the given location.
    """
    location = models.ForeignKey(Location)
    lead = models.ForeignKey(User)

class Resource(models.Model):
    """
    Generic resources for locations.
    """
    location = models.ForeignKey(Location)
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=200, blank=True)

class Award(models.Model):
    location = models.ForeignKey(Location)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="awards", blank=True)
    project = models.ManyToManyField(Project)
