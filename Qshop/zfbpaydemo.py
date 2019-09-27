from alipay import AliPay
## 公钥
alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtexG8P2qyi04DUrUEQnbpfCYS7im27E0q55gsDiE+g/JdWwJJ3/I2PRPbyz38ah2mv66GFdE4j2nXarL3jSgoP995mZzmllGLDSOWbFI2QB+7ZMikVFXzjWZ68FcQMEJExuC7ikD4vuY8J4Wt00NerbSwKCWL4CjvV3CxcBaJXPn3kIOzItX0yDToK9rvZ9E4P1PIURe96Q/SNz+GkJaR32PQJotUOrsg0gVdWhSBIjRuSpvUpUlPEZrzprhyYn/zZ6TktKaURzfVqSpRa0h+Z9y03sIIDVLSWRlaDKw81WsVKfJlUcN9WA/uypMOOQb6MXolZEYMRm+EDgEFT0oUQIDAQAB
-----END PUBLIC KEY-----"""
## 私钥
alipay_private_key_string="""-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAtexG8P2qyi04DUrUEQnbpfCYS7im27E0q55gsDiE+g/JdWwJJ3/I2PRPbyz38ah2mv66GFdE4j2nXarL3jSgoP995mZzmllGLDSOWbFI2QB+7ZMikVFXzjWZ68FcQMEJExuC7ikD4vuY8J4Wt00NerbSwKCWL4CjvV3CxcBaJXPn3kIOzItX0yDToK9rvZ9E4P1PIURe96Q/SNz+GkJaR32PQJotUOrsg0gVdWhSBIjRuSpvUpUlPEZrzprhyYn/zZ6TktKaURzfVqSpRa0h+Z9y03sIIDVLSWRlaDKw81WsVKfJlUcN9WA/uypMOOQb6MXolZEYMRm+EDgEFT0oUQIDAQABAoIBAGDUC8ZFHdxSSR06ELmo55HhBw52j8kq/n/B4nCpBI4cTPwErrKpXvuqvYTNCINFSSuiHObLvEw2yJggSjZRCJXoptg0+57RmXn51zKCG+X0T5qfz6xNAVEuUmibGEEW/X+ACyY8CmeLxpF7c1fI2T3RhUclsgpCi+REvWCHyvNXYIj5S8c3+KBXGzdmmwv97PTtkkMW4K2QDG9wcimZU/stUrtsx8vBm9T4TmDz3BiXnCHoJDJCx5j9R8MlrT2hD2HdwxjZzMNBveHNdDK2mWrCVnzNzJiUnBPxh0ObJU+Qf9g32Gmyn/8QZbRDDiN6az+NWiMJx/ikPQTB4QWdYckCgYEA8YSEAVCU8bTmRDS//uOB6sGzt1KDG3fmTuSuupoJT4FC7UiUg0eo3ZfvqHrowkVccEgRgKCtUpWNrR1SzheXvc8QajeLqGP3dk5vI2naseqCE1nhqW0i8BRezjrPiWxkzG4aNO2BLTco+ZV7AJYW0E0hMW2YDu9kqrCRzV2PVZcCgYEAwNTvwwEFW2LZwv8gzITqg9S71phz0u4DSvkvlm57FO2G/RWwp5S7ukvLPgOgVHVymFsfUQy2J0HcvqFysvyJulj+PHK9onddnm8msrLsUG66ui1QrIUP06p2v98IaG2jKJxFCX79XPr67UgKXq8kX/s491NkHq774pdUy9InvlcCgYBnp2b8JXh3MBtvhHAuVbgpZ87Yy/nm7ROUIoN3JKsAS0rNCcxrd3La/91korOIxToCGnwgh1U7z2HJvX8PYoLGfLrfy00ODTFkvg7m1QR+PVZsNbQrAeLvxN5XhlgR88pjDpICyzgYjsbwLx5mRwQtjBzF2PJc3pOGylcZG6FrqwKBgQCUoQwU0Cqi37RdGmzbdu+ToVsO8v8Da7VaCmtllc6EuPg9BoTdBkUUOOt05zKjJsunJ0UiIZwc8iUFQke4MfKukX2UdhQ4r6yXO7EmN8bx0AdZDSiLcRxb154kEfLXGvqRiLGluh3rlv/l+IsVpAVzfZ3Q9JPNGq7HXkFbwKYljQKBgGO9dozcq7hspOEsM+tlN2Z21SxM3mK+udOntXw+xD3iSbksiI9GOmHs09Np/95TN21lwl1h7r40/5rxC6s0cfrPd+7c0QhsgM9yOE1onkazY5DLmGDaW979HZLuB1y4V2ksw2ttJfirRtHPYRBcHS/XVmEzTUGk4zfqA4lkQ15x
-----END RSA PRIVATE KEY-----"""
## 实例化支付对象
alipay = AliPay(
    appid='2016101300673940',
    app_notify_url = None,
    app_private_key_string=alipay_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",
)
## 实例化订单
order_string = alipay.api_alipay_trade_page_pay(
    subject = '牛羊生鲜',   ## 交易主题
    out_trade_no = "10000000002",    ## 订单号
    total_amount = '100',     ## 交易总金额
    return_url=None,         ##  请求支付，之后及时回调的一个接口
    notify_url=None          ##  通知地址，
)



##   发送支付请求
## 请求地址  支付网关 + 实例化订单
result = "https://openapi.alipaydev.com/gateway.do?"+order_string
print(result)


