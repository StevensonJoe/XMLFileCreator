# XMLFileCreator
Create specifically formatted XML files for batch upload of transport request slots.

### Input
Container Number, Delivery Date, Delivery Time, Delivery Site Code, Site Name separated by newline e.g.

	CPSU6401913    20-Nov-19    15:00    SITE0001    SITE1
	TGHU6401913    22-Nov-19    19:00    SITE0002    SITE2
	MRKU6401913    21-Nov-19    18:00    SITE0003    SITE3

### Output
XML file containing the above information split into nodes. See example file for file output.
