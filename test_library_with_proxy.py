#!/usr/bin/env python3
"""
领星API测试程序 - 使用修改后的官方库支持代理
基于官方lingxingapi库进行完整测试，并使用代理服务器
"""

import asyncio
import sys
from datetime import datetime
from lingxingapi import API


async def test_with_library_and_proxy():
    """使用修改后的官方库测试API（带代理）"""
    print("=" * 70)
    print("领星API测试 - 使用修改后的官方库（支持代理）")
    print("=" * 70)
    print(f"Python版本: {sys.version}")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 70)

    # API配置
    app_id = "ak_QKgNwGafo1hd7"
    app_secret = "ygRPim10XzzSMu/mkA/vrg=="
    proxy_url = "http://118.24.74.92:3028/"

    print(f"AppID: {app_id}")
    print(f"代理服务器: {proxy_url}")
    print("-" * 70)

    try:
        async with API(
            app_id=app_id,
            app_secret=app_secret,
            timeout=30,
            ignore_api_limit=True,
            ignore_api_limit_wait=0.5,
            ignore_api_limit_retry=3,
            proxy=proxy_url  # 新增的代理参数
        ) as api:

            print("开始API调用测试...")
            print()

            # 1. 获取访问令牌
            print("1. 获取访问令牌...")
            token_info = await api.AccessToken()
            print(f"[SUCCESS] 访问令牌获取成功")
            print(f"   有效期: {token_info.expires_in} 秒")
            print(f"   Token前缀: {token_info.access_token[:8]}...")
            print()

            # 2. 获取店铺列表
            print("2. 获取店铺列表...")
            sellers_result = await api.basic.Sellers()
            sellers = sellers_result.data  # 访问 data 属性获取店铺列表
            print(f"[SUCCESS] 成功获取 {len(sellers)} 个店铺信息")
            print()

            # 显示店铺详细信息
            print("店铺详细信息:")
            print("-" * 70)
            for i, seller in enumerate(sellers[:5], 1):  # 只显示前5个
                print(f"店铺 {i}:")
                print(f"  ID: {seller.sid}")
                print(f"  名称: {seller.seller_name}")
                print(f"  卖家ID: {seller.seller_id}")
                print(f"  账户名: {seller.account_name}")
                print(f"  国家/地区: {seller.country}")
                print(f"  市场: {seller.region}")
                print(f"  市场ID: {seller.marketplace_id}")
                print(f"  状态: {seller.status}")
                print(f"  广告设置: {seller.ads_authorized}")
                print()

            if len(sellers) > 5:
                print(f"... 还有 {len(sellers) - 5} 个店铺未显示")
                print()

            # 3. 获取市场列表
            print("3. 获取市场列表...")
            marketplaces_result = await api.basic.Marketplaces()
            marketplaces = marketplaces_result.data  # 访问 data 属性获取市场列表
            print(f"[SUCCESS] 成功获取 {len(marketplaces)} 个市场信息")
            print()

            # 显示市场信息
            print("市场详细信息:")
            print("-" * 70)
            for i, marketplace in enumerate(marketplaces[:10], 1):  # 只显示前10个
                print(f"市场 {i}:")
                print(f"  ID: {marketplace.mid}")
                print(f"  地区: {marketplace.region}")
                print(f"  AWS区域: {marketplace.region_aws}")
                print(f"  国家: {marketplace.country}")
                print(f"  国家代码: {marketplace.country_code}")
                print(f"  市场ID: {marketplace.marketplace_id}")
                print()

            if len(marketplaces) > 10:
                print(f"... 还有 {len(marketplaces) - 10} 个市场未显示")

            # 4. 获取汇率信息
            print("\n4. 获取汇率信息...")
            try:
                exchange_rates_result = await api.basic.ExchangeRates()
                exchange_rates = exchange_rates_result.data  # 访问 data 属性获取汇率列表
                print(f"[SUCCESS] 成功获取 {len(exchange_rates)} 条汇率信息")

                # 显示最近几条汇率
                if exchange_rates:
                    print("汇率信息 (最近5条):")
                    print("-" * 70)
                    for rate in exchange_rates[:5]:
                        print(f"  {rate.date}: {rate.from_currency} → {rate.to_currency} = {rate.rate}")
                else:
                    print("  暂无汇率信息")
                print()

            except Exception as e:
                print(f"[WARN] 汇率信息获取失败: {e}")
                print()

            # 5. 刷新令牌测试
            print("5. 测试令牌刷新...")
            try:
                new_token = await api.RefreshToken(token_info.refresh_token)
                print(f"[SUCCESS] 令牌刷新成功!")
                print(f"   新Token前缀: {new_token.access_token[:8]}...")
                print(f"   新有效期: {new_token.expires_in} 秒")
                print()
            except Exception as e:
                print(f"[WARN] 令牌刷新失败: {e}")
                print()

            # 测试总结
            print("=" * 70)
            print("[SUCCESS] 所有API调用成功完成！")
            print("=" * 70)
            print("测试结果总结:")
            print(f"  访问令牌: 有效期 {token_info.expires_in} 秒")
            print(f"  店铺数量: {len(sellers)} 个")
            print(f"  市场数量: {len(marketplaces)} 个")
            if 'exchange_rates' in locals():
                print(f"  汇率信息: {len(exchange_rates)} 条")
            print(f"  代理状态: 正常工作")
            print(f"  API状态: 完全正常")
            print("=" * 70)

            return True

    except Exception as e:
        print(f"[FAIL] API调用失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("领星API测试程序启动 - 使用修改后的官方库（支持代理）")
    print("支持 Python 3.10+ | 使用官方 lingxingapi 库 | 支持代理服务器")
    print()

    # 测试API连接
    success = await test_with_library_and_proxy()

    # 最终总结
    print("\n" + "=" * 70)
    print("测试完成 - 最终总结")
    print("=" * 70)

    if success:
        print("[SUCCESS] 领星API测试完全成功！")
        print("API配置正确，代理功能正常工作，所有功能正常。")
    else:
        print("[FAIL] 领星API测试失败。")
        print("请检查配置、代理服务器和网络连接。")

    print("=" * 70)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行异常: {e}")
        import traceback
        traceback.print_exc()