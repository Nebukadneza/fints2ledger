from fints.client import NeedTANResponse

class TRetriever:
    def __init__(self, client, accountnumber):
        self.client = client
        self.accountnumber = accountnumber

    def get_hbci_transactions(self, start_date, end_date):
        with self.client:
            accounts = self.client.get_sepa_accounts()
            account = self.__find_matching_account(accounts, self.accountnumber)
            transactions = self.client.get_transactions(account, start_date, end_date)
            if type(transactions) is NeedTANResponse:
                tan = input(transactions.challenge)
                lol = self.client.send_tan(transactions, tan)
                transactions = self.client.get_transactions(account, start_date, end_date)
        return transactions

    def __find_matching_account(self, accounts, accountnumber):
        for account in accounts:
            if account.accountnumber == accountnumber:
                return account
        raise Exception("Could not find a matching account for account number '{missing_account}'. Possible accounts: {accounts}"
                        .format(missing_account=accountnumber, accounts=accounts))
