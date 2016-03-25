from necessary_import import *

class strat2(StrategyDesign):        

    def __init__(self, context, name = 'stupid momentum strategy on SPY', instruments=None):
        StrategyDesign.__init__(self, name)

        self.context = context
        self.lookback = 3*21 # 4 months period, 21 trading days per month

        if instruments is None:        
            self.instruments = {'equity':symbol('SPY')}
       
        self.add_schedule_function( context.schedule_function(self.rebalance,
                      date_rule=date_rules.month_start(),
                      time_rule=time_rules.market_open(hours=1, minutes=0))
        )

        '''
        Analytics Manager
        '''
        self.create_analytics (name='allocation', columns=['timestamp', 'equity', 'mom'])
        return
        
    def abs_mom_up (self, data):
        inst = self.instruments.values()[0]
        
        prices = history(self.lookback, '1d', 'price')
        NbNan = np.count_nonzero(np.isnan(prices))
        if NbNan > 0:
            return -1
                
        mom = prices.mean()
        if data[inst].price > mom[inst]:
            return 1
        else:
            return 0
            
    def rebalance (self, context, data):
        inst = self.instruments.values()[0]        
        mom = self.abs_mom_up(data)
        if mom == -1:
            return
        
        # mom = -1 if Nan values
        target_percent_dict = dict()
        if mom == 1:
            target_percent_dict[inst] = 1
            msg = "\n TOY EXAMPLE MSG \t"+str(get_datetime().date()) + " - Long SPY: " 
            self.add_log('info',msg)
        elif mom == 0:
            target_percent_dict[inst] = 0
            msg = "\n TOY EXAMPLE MSG \t"+str(get_datetime().date()) + " - Exit SPY: "
            self.add_log('info',msg)
            
        '''
        dumping anaytics: toy example as no value logging mom as-is
        '''
        if self.get_dumpanalytics():
            # columns=['timestamp', 'equity', 'treasury']
            row = [get_datetime().date(), target_percent_dict[self.instruments['equity']],
                   mom]
            self.insert_analyticsdata('allocation',row)
        
        self.send_percent_orders(data, target_percent_dict)
        return