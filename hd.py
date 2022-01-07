

 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90

	

import requests

### get cookies ###
s = requests.Session()

headers = 	{
	'accept':'*/*',
	'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
	}

land = s.get('https://www.homedepot.com/',headers=headers)

print(land)

headers = 	{
	'accept':'*/*',
	'accept-encoding':'gzip, deflate, br',
	'accept-language':'en-US,en;q=0.9',
	'apollographql-client-name':'general-merchandise',
	'apollographql-client-version':'0.0.0',
	'cache-control':'no-cache',
	'content-length':'7802',
	'content-type':'application/json',
	'dnt':'1',
	'origin':'https://www.homedepot.com',
	'pragma':'no-cache',
	'referer':'https://www.homedepot.com/p/2-in-x-4-in-x-96-in-Prime-Whitewood-Stud-058449/312528776',
	'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
	'sec-ch-ua-mobile':'?0',
	'sec-ch-ua-platform':'"Windows"',
	'sec-fetch-dest':'empty',
	'sec-fetch-mode':'cors',
	'sec-fetch-site':'same-origin',
	'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
	'x-api-cookies':'{}',
	'x-current-url':'/p/2-in-x-4-in-x-96-in-Prime-Whitewood-Stud-058449/312528776',
	'x-debug':'false',
	'x-experience-name':'general-merchandise',
	'x-hd-dc':'origin'
	}

### store code scrape ###

starting_store_code = 2109 #go to home depot and get your local store code I guess, I imagine you have more store codes than this gets
radius = 600 #seems to break for higher values
pagesize = 30 #max 30 :(
pages = 1 #can scape more pages if needed

stores_codes = []
for page in range(1,pages+1):

	stores_url = f'https://www.homedepot.com/StoreSearchServices/v2/storesearch?address={starting_store_code}&radius={radius}&pagesize={pagesize}'
	stores = s.get(stores_url,headers=headers).json()

	for store in stores['stores']:
		stores_codes.append(store['storeId'])

print(f'# of Stores: {len(stores_codes)}')
###

### load a text file of product codes ###

#this is an example with each line being a product code, you probably have a list of these already?

with open('prod_codes.txt','r') as f:
    prods = [line.rstrip() for line in f.readlines()] #get rid of newline character

print(f'# of Products: {len(prods)}')
###

### time to spam their servers

for store_code in stores_codes:
	for prod in prods:

		query = {
			"operationName":"productClientOnlyProduct","variables":{
				"skipSpecificationGroup":False,"skipSubscribeAndSave":False,"skipKPF":False,"itemId":str(prod),"storeId":str(store_code),"zipCode":"75209" #not sure we need to change zip?
				},
			"query":"query productClientOnlyProduct($storeId: String, $zipCode: String, $itemId: String!, $dataSource: String, $loyaltyMembershipInput: LoyaltyMembershipInput, $skipSpecificationGroup: Boolean = false, $skipSubscribeAndSave: Boolean = false, $skipKPF: Boolean = false) {\n  product(itemId: $itemId, dataSource: $dataSource, loyaltyMembershipInput: $loyaltyMembershipInput) {\n    fulfillment(storeId: $storeId, zipCode: $zipCode) {\n      backordered\n      fulfillmentOptions {\n        type\n        services {\n          type\n          locations {\n            isAnchor\n            inventory {\n              isLimitedQuantity\n              isOutOfStock\n              isInStock\n              quantity\n              isUnavailable\n              maxAllowedBopisQty\n              minAllowedBopisQty\n              __typename\n            }\n            type\n            storeName\n            locationId\n            curbsidePickupFlag\n            isBuyInStoreCheckNearBy\n            distance\n            state\n            storePhone\n            __typename\n          }\n          deliveryTimeline\n          deliveryDates {\n            startDate\n            endDate\n            __typename\n          }\n          deliveryCharge\n          dynamicEta {\n            hours\n            minutes\n            __typename\n          }\n          hasFreeShipping\n          freeDeliveryThreshold\n          totalCharge\n          __typename\n        }\n        fulfillable\n        __typename\n      }\n      anchorStoreStatus\n      anchorStoreStatusType\n      backorderedShipDate\n      bossExcludedShipStates\n      sthExcludedShipState\n      bossExcludedShipState\n      excludedShipStates\n      seasonStatusEligible\n      onlineStoreStatus\n      onlineStoreStatusType\n      inStoreAssemblyEligible\n      __typename\n    }\n    info {\n      dotComColorEligible\n      hidePrice\n      ecoRebate\n      quantityLimit\n      sskMin\n      sskMax\n      unitOfMeasureCoverage\n      wasMaxPriceRange\n      wasMinPriceRange\n      fiscalYear\n      productDepartment\n      classNumber\n      forProfessionalUseOnly\n      globalCustomConfigurator {\n        customButtonText\n        customDescription\n        customExperience\n        customExperienceUrl\n        customTitle\n        __typename\n      }\n      paintBrand\n      movingCalculatorEligible\n      label\n      prop65Warning\n      returnable\n      recommendationFlags {\n        visualNavigation\n        reqItems\n        batItems\n        __typename\n      }\n      replacementOMSID\n      hasSubscription\n      minimumOrderQuantity\n      projectCalculatorEligible\n      subClassNumber\n      calculatorType\n      isLiveGoodsProduct\n      protectionPlanSku\n      hasServiceAddOns\n      consultationType\n      __typename\n    }\n    itemId\n    dataSources\n    identifiers {\n      canonicalUrl\n      brandName\n      itemId\n      modelNumber\n      productLabel\n      storeSkuNumber\n      upcGtin13\n      specialOrderSku\n      toolRentalSkuNumber\n      rentalCategory\n      rentalSubCategory\n      upc\n      productType\n      isSuperSku\n      parentId\n      roomVOEnabled\n      sampleId\n      __typename\n    }\n    availabilityType {\n      discontinued\n      status\n      type\n      buyable\n      __typename\n    }\n    details {\n      description\n      collection {\n        url\n        collectionId\n        __typename\n      }\n      highlights\n      descriptiveAttributes {\n        name\n        value\n        bulleted\n        sequence\n        __typename\n      }\n      infoAndGuides {\n        name\n        url\n        __typename\n      }\n      installation {\n        leadGenUrl\n        __typename\n      }\n      __typename\n    }\n    media {\n      images {\n        url\n        type\n        subType\n        sizes\n        __typename\n      }\n      video {\n        shortDescription\n        thumbnail\n        url\n        videoStill\n        link {\n          text\n          url\n          __typename\n        }\n        title\n        type\n        videoId\n        longDescription\n        __typename\n      }\n      threeSixty {\n        id\n        url\n        __typename\n      }\n      augmentedRealityLink {\n        usdz\n        image\n        __typename\n      }\n      richContent {\n        content\n        __typename\n      }\n      __typename\n    }\n    pricing(storeId: $storeId) {\n      promotion {\n        dates {\n          end\n          start\n          __typename\n        }\n        type\n        description {\n          shortDesc\n          longDesc\n          __typename\n        }\n        dollarOff\n        percentageOff\n        savingsCenter\n        savingsCenterPromos\n        specialBuySavings\n        specialBuyDollarOff\n        specialBuyPercentageOff\n        experienceTag\n        subExperienceTag\n        anchorItemList\n        itemList\n        reward {\n          tiers {\n            minPurchaseAmount\n            minPurchaseQuantity\n            rewardPercent\n            rewardAmountPerOrder\n            rewardAmountPerItem\n            rewardFixedPrice\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      value\n      alternatePriceDisplay\n      alternate {\n        bulk {\n          pricePerUnit\n          thresholdQuantity\n          value\n          __typename\n        }\n        unit {\n          caseUnitOfMeasure\n          unitsOriginalPrice\n          unitsPerCase\n          value\n          __typename\n        }\n        __typename\n      }\n      original\n      mapAboveOriginalPrice\n      message\n      preferredPriceFlag\n      specialBuy\n      unitOfMeasure\n      __typename\n    }\n    reviews {\n      ratingsReviews {\n        averageRating\n        totalReviews\n        __typename\n      }\n      __typename\n    }\n    seo {\n      seoKeywords\n      seoDescription\n      __typename\n    }\n    specificationGroup @skip(if: $skipSpecificationGroup) {\n      specifications {\n        specName\n        specValue\n        __typename\n      }\n      specTitle\n      __typename\n    }\n    taxonomy {\n      breadCrumbs {\n        label\n        url\n        browseUrl\n        creativeIconUrl\n        deselectUrl\n        dimensionName\n        refinementKey\n        __typename\n      }\n      brandLinkUrl\n      __typename\n    }\n    favoriteDetail {\n      count\n      __typename\n    }\n    sizeAndFitDetail {\n      attributeGroups {\n        attributes {\n          attributeName\n          dimensions\n          __typename\n        }\n        dimensionLabel\n        productType\n        __typename\n      }\n      __typename\n    }\n    subscription @skip(if: $skipSubscribeAndSave) {\n      defaultfrequency\n      discountPercentage\n      subscriptionEnabled\n      __typename\n    }\n    badges(storeId: $storeId) {\n      label\n      color\n      creativeImageUrl\n      endDate\n      message\n      name\n      timerDuration\n      timer {\n        timeBombThreshold\n        daysLeftThreshold\n        dateDisplayThreshold\n        message\n        __typename\n      }\n      __typename\n    }\n    keyProductFeatures @skip(if: $skipKPF) {\n      keyProductFeaturesItems {\n        features {\n          name\n          refinementId\n          refinementUrl\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    seoDescription\n    installServices {\n      scheduleAMeasure\n      __typename\n    }\n    dataSource\n    __typename\n  }\n}\n"}

		url = 'https://www.homedepot.com/federation-gateway/graphql?opname=productClientOnlyProduct'

		resp = s.post(url,headers=headers,json=query).json()

		name = resp['data']['product']['identifiers']['productLabel']
		price = resp['data']['product']['pricing']['value']
		stock = resp['data']['product']['fulfillment']['fulfillmentOptions'][0]['services'][0]['locations'][0]['inventory']['quantity']

		print(f'Price: {str(price)}   Stock: {str(stock)}   Store: {str(store_code)}   Product: {name}')

