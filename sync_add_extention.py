from googleads import adwords


PAGE_SIZE = 100


class GoogleAdWords:

    def __init__(self):
        self.client = adwords.AdWordsClient.LoadFromStorage()

    def get_campaign_ids(self):

        campaign_service = self.client.GetService('CampaignService', version='v201710')
        # Construct selector and get all campaigns.
        selector = {
            'fields': ['Id', 'Name', 'Status']
        }
        campaigns = campaign_service.get(selector)
        campaign_ids = []
        if 'entries' in campaigns:
            for campaign in campaigns['entries']:
                campaign_ids.append(campaign['id'])
        else:
            print
            'No campaigns were found.'
            return
        return campaign_ids

    def get_ad_group_ids(self, campaign_id):
        ad_group_service = self.client.GetService('AdGroupService', version='v201710')

        # Construct selector and get all ad groups.
        offset = 0
        selector = {
            'fields': ['Id', 'Name', 'Status'],
            'predicates': [
                {
                    'field': 'CampaignId',
                    'operator': 'EQUALS',
                    'values': [campaign_id]
                }
            ],
            'paging': {
                'startIndex': str(offset),
                'numberResults': str(PAGE_SIZE)
            }
        }
        more_pages = True
        ad_group_ids = []
        while more_pages:
            page = ad_group_service.get(selector)

            # Display results.
            if 'entries' in page:
                for ad_group in page['entries']:
                    print ('Ad group with name "%s", id "%s" and status "%s" was '
                           'found.' % (ad_group['name'], ad_group['id'],
                                       ad_group['status']))
                    ad_group_ids.append(ad_group['id'])
            else:
                print 'No ad groups were found.'
            offset += PAGE_SIZE
            selector['paging']['startIndex'] = str(offset)
            more_pages = offset < int(page['totalNumEntries'])
        return ad_group_ids

    def update_ad_group(self, ad_group_id):
        ad_group_extension_setting_service = self.client.GetService('AdGroupExtensionSettingService', version='v201710')
        promotion = GoogleAdWords.create_promotion()

        ad_group_extension_setting = {
            'adGroupId': ad_group_id,
            'extensionType': 'PROMOTION',
            'extensionSetting': {
                'extensions': [promotion]
            }
        }

        operation = {
            'operator': 'ADD',
            'operand': ad_group_extension_setting
        }

        ad_group_extension_setting_service.mutate(operation)

    @staticmethod
    def create_promotion():

        return {
            'xsi_type': 'PromotionFeedItem',
            'language': 'en',
            'promotionStart' : '' ,
            'promotionEnd' : '' ,
            'promotionTarget': 'Wool Socks',
            'percentOff': 10000000,
            'promotionCode': 'WinterSocksDeal',
            'finalUrls': {
                'urls': ['http://www.example.com/socks']
            }
        }


if __name__ == '__main__':
    google_adwords = GoogleAdWords()
    ad_grp_ids = google_adwords.get_ad_group_ids(campaign_id="1")
    google_adwords.update_ad_group(ad_group_id="1")