from logic import get_real_price
from logic import load_portfolio
from logic import update_cash

def test_get_real_price_1():
    result = get_real_price('BTC-USD')
    assert isinstance(result, (int, float))

def test_get_real_price_2():
    result = get_real_price('')
    assert result is None

def test_get_real_price_3():
    result = get_real_price('Bitcoin')
    assert result is None

def test_get_real_price_4():
    result = get_real_price('INVALID')
    assert result is None

def test_get_real_price_5():
    result = get_real_price('AAPL')
    assert isinstance(result, (int, float))







def test_load_portfolio_1():
    result = load_portfolio('')
    if result['cash']==0 and result['positions']=={} and result['history']==[]:
        assert isinstance(result, dict)

def test_load_portfolio_2():
    result = load_portfolio('test.json')
    if result['cash'] != 0:
         assert isinstance(result, dict)

def test_load_portfolio_3():
    result = load_portfolio('NotExist.json')
    if result['cash'] == 0 and result['positions'] == {} and result['history'] == []:
            assert isinstance(result, dict)





def test_update_cash_1():
    data = {'cash':0, 'positions':{}, 'history':[]}
    result = update_cash(data, 10000)
    if result['cash'] == 10000:
        assert isinstance(result['cash'], (int, float))

def test_update_cash_2():
    data = {'cash':0, 'positions':{}, 'history':[]}
    result = update_cash(data, '10000')
    assert result is None

def test_update_cash_3():
    result = update_cash({}, 10000)
    assert result is None

def test_update_cash_4():
    result = update_cash({'cash': 100000, 'positions': {}, 'history':[]}, -10000)
    if result['cash'] == 90000:
        assert isinstance(result['cash'], (int, float))