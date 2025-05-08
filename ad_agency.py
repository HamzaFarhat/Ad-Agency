import datetime

class Campaign:
    def __init__(self, name, active=True, dayparting=None):
        self.name = name
        self.active = active
        self.dayparting = dayparting  # Tuple of (start_hour, end_hour)

    def should_run(self, current_hour):
        if self.dayparting:
            start, end = self.dayparting
            return start <= current_hour < end
        return True

    def turn_off(self):
        self.active = False

    def turn_on(self):
        self.active = True


class Brand:
    def __init__(self, name, monthly_budget, daily_budget):
        self.name = name
        self.monthly_budget = monthly_budget
        self.daily_budget = daily_budget
        self.campaigns = []
        self.daily_spend = 0.0
        self.monthly_spend = 0.0
        self.last_reset_date = datetime.date.today()

    def add_campaign(self, campaign):
        self.campaigns.append(campaign)

    def accumulate_spend(self, amount):
        self.daily_spend += amount
        self.monthly_spend += amount
        self.check_budgets()

    def check_budgets(self):
        if self.daily_spend >= self.daily_budget or self.monthly_spend >= self.monthly_budget:
            self.turn_off_all_campaigns()

    def reset_budgets_if_needed(self):
        today = datetime.date.today()
        if today.day != self.last_reset_date.day:
            self.daily_spend = 0.0
            self.turn_on_all_campaigns_if_budget_allows()
        if today.month != self.last_reset_date.month:
            self.monthly_spend = 0.0
            self.turn_on_all_campaigns_if_budget_allows()
        self.last_reset_date = today

    def turn_off_all_campaigns(self):
        for campaign in self.campaigns:
            campaign.turn_off()

    def turn_on_all_campaigns_if_budget_allows(self):
        if self.daily_spend < self.daily_budget and self.monthly_spend < self.monthly_budget:
            for campaign in self.campaigns:
                campaign.turn_on()

    def enforce_dayparting(self):
        current_hour = datetime.datetime.now().hour
        for campaign in self.campaigns:
            if campaign.should_run(current_hour):
                if self.daily_spend < self.daily_budget and self.monthly_spend < self.monthly_budget:
                    campaign.turn_on()
            else:
                campaign.turn_off()

    def get_status(self):
        return {
            'brand': self.name,
            'daily_spend': self.daily_spend,
            'monthly_spend': self.monthly_spend,
            'campaigns': [
                {'name': c.name, 'active': c.active, 'dayparting': c.dayparting}
                for c in self.campaigns
            ]
        }


# Example usage
if __name__ == "__main__":
    brand = Brand("BrandA", monthly_budget=5000, daily_budget=200)
    brand.add_campaign(Campaign("Campaign1", dayparting=(1, 2)))
    brand.add_campaign(Campaign("Campaign2"))

    brand.reset_budgets_if_needed()
    brand.accumulate_spend(100)
    brand.enforce_dayparting()
    print(brand.get_status())
