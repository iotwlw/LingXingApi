#!/usr/bin/env python3
"""
配置管理模块
用于加载和管理API配置、代理设置等
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器

        :param config_file: 配置文件路径
        """
        self.config_file = Path(config_file)
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            else:
                raise FileNotFoundError(f"配置文件 {self.config_file} 不存在")
        except json.JSONDecodeError as e:
            raise ValueError(f"配置文件格式错误: {e}")
        except Exception as e:
            raise RuntimeError(f"加载配置文件失败: {e}")

    @property
    def app_id(self) -> str:
        """获取应用ID"""
        return self._config.get("api", {}).get("app_id", "")

    @property
    def app_secret(self) -> str:
        """获取应用密钥"""
        return self._config.get("api", {}).get("app_secret", "")

    @property
    def proxy_enabled(self) -> bool:
        """是否启用代理"""
        return self._config.get("proxy", {}).get("enabled", False)

    @property
    def proxy_url(self) -> Optional[str]:
        """获取代理URL"""
        if not self.proxy_enabled:
            return None

        proxy_config = self._config.get("proxy", {})
        # 优先使用HTTPS代理，如果不存在则使用HTTP代理
        return proxy_config.get("https_url") or proxy_config.get("http_url")

    @property
    def timeout(self) -> int:
        """获取超时设置"""
        return self._config.get("settings", {}).get("timeout", 30)

    @property
    def ignore_api_limit(self) -> bool:
        """是否忽略API限流"""
        return self._config.get("settings", {}).get("ignore_api_limit", False)

    @property
    def ignore_api_limit_wait(self) -> float:
        """忽略API限流时的等待时间"""
        return self._config.get("settings", {}).get("ignore_api_limit_wait", 0.2)

    @property
    def ignore_api_limit_retry(self) -> int:
        """忽略API限流时的重试次数"""
        return self._config.get("settings", {}).get("ignore_api_limit_retry", 60)

    def validate_config(self) -> bool:
        """验证配置是否完整"""
        errors = []

        # 验证API配置
        if not self.app_id:
            errors.append("缺少 app_id 配置")
        if not self.app_secret:
            errors.append("缺少 app_secret 配置")

        # 验证代理配置（如果启用）
        if self.proxy_enabled and not self.proxy_url:
            errors.append("启用代理但缺少代理URL配置")

        if errors:
            print("配置验证失败:")
            for error in errors:
                print(f"  - {error}")
            return False

        return True

    def print_config_summary(self) -> None:
        """打印配置摘要"""
        print("=" * 50)
        print("配置信息摘要")
        print("=" * 50)
        print(f"应用ID: {self.app_id[:10]}...")
        print(f"应用密钥: {self.app_secret[:10]}...")
        print(f"代理状态: {'启用' if self.proxy_enabled else '禁用'}")
        if self.proxy_enabled:
            print(f"代理URL: {self.proxy_url}")
        print(f"请求超时: {self.timeout} 秒")
        print(f"忽略限流: {'是' if self.ignore_api_limit else '否'}")
        if self.ignore_api_limit:
            print(f"限流等待: {self.ignore_api_limit_wait} 秒")
            print(f"限流重试: {self.ignore_api_limit_retry} 次")
        print("=" * 50)


# 全局配置实例
_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_file: str = "config.json") -> ConfigManager:
    """获取全局配置管理器实例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_file)
    return _config_manager


def reload_config(config_file: str = "config.json") -> ConfigManager:
    """重新加载配置"""
    global _config_manager
    _config_manager = ConfigManager(config_file)
    return _config_manager


if __name__ == "__main__":
    # 测试配置管理器
    try:
        config = get_config_manager()
        if config.validate_config():
            config.print_config_summary()
            print("配置加载成功！")
        else:
            print("配置验证失败！")
    except Exception as e:
        print(f"配置加载错误: {e}")