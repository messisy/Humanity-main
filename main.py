from web3 import Web3
from colorama import init, Fore
import sys
import time
from datetime import datetime
import requests
from urllib.parse import urlparse
import os

# 初始化 colorama
init(autoreset=True)

class HumanityProtocolBot:
    def __init__(self):
        self.rpc_url = 'https://rpc.testnet.humanity.org'
        self.contract_address = '0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7'
        self.contract_abi = [
            {"inputs":[],"name":"AccessControlBadConfirmation","type":"error"},
            {"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"bytes32","name":"neededRole","type":"bytes32"}],"name":"AccessControlUnauthorizedAccount","type":"error"},
            {"inputs":[],"name":"InvalidInitialization","type":"error"},
            {"inputs":[],"name":"NotInitializing","type":"error"},
            {"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},
            {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"bool","name":"bufferSafe","type":"bool"}],"name":"ReferralRewardBuffered","type":"event"},
            {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"enum IRewards.RewardType","name":"rewardType","type":"uint8"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardClaimed","type":"event"},
            {"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},
            {"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},
            {"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},
            {"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
            {"inputs":[],"name":"claimBuffer","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[],"name":"claimReward","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[],"name":"currentEpoch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
            {"inputs":[],"name":"cycleStartTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"internalType":"address","name":"vcContract","type":"address"},{"internalType":"address","name":"tkn","type":"address"}],"name":"init","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"callerConfirmation","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"internalType":"uint256","name":"startTimestamp","type":"uint256"}],"name":"start","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[],"name":"stop","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userBuffer","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"epochID","type":"uint256"}],"name":"userClaimStatus","outputs":[{"components":[{"internalType":"uint256","name":"buffer","type":"uint256"},{"internalType":"bool","name":"claimStatus","type":"bool"}],"internalType":"struct IRewards.UserClaim","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userGenesisClaimStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}
        ]

    @staticmethod
    def current_time():
        """返回当前时间的格式化字符串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def load_accounts_data():
        """加载私钥和对应的代理"""
        accounts_data = []

        try:
            with open('private_keys.txt', 'r') as f:
                private_keys = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(Fore.RED + "错误: 找不到 private_keys.txt 文件")
            sys.exit(1)

        try:
            with open('proxy.txt', 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(Fore.YELLOW + "未找到 proxy.txt 文件，所有账号将使用直连")
            proxies = [''] * len(private_keys)

        if len(proxies) < len(private_keys):
            print(Fore.YELLOW + f"代理数量({len(proxies)})少于私钥数量({len(private_keys)})，部分账号将使用直连")
            proxies.extend([''] * (len(private_keys) - len(proxies)))

        for private_key, proxy in zip(private_keys, proxies):
            accounts_data.append({
                'private_key': private_key,
                'proxy': proxy
            })

        return accounts_data

    @staticmethod
    def format_proxy(proxy):
        """格式化代理字符串"""
        if not proxy:
            return None
        
        try:
            if proxy.startswith('socks5://'):
                return {'http': proxy, 'https': proxy}
            elif proxy.startswith('http://') or proxy.startswith('https://'):
                return {'http': proxy, 'https': proxy}
            else:
                return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        except Exception as e:
            print(Fore.RED + f"代理格式化错误: {str(e)}")
            return None

    def setup_blockchain_connection(self, proxy=None):
        """建立区块链连接"""
        try:
            if proxy:
                formatted_proxy = self.format_proxy(proxy)
                if formatted_proxy:
                    session = requests.Session()
                    session.proxies = formatted_proxy
                    web3 = Web3(Web3.HTTPProvider(
                        self.rpc_url,
                        session=session,
                        request_kwargs={"timeout": 30}
                    ))
                else:
                    web3 = Web3(Web3.HTTPProvider(self.rpc_url))
            else:
                web3 = Web3(Web3.HTTPProvider(self.rpc_url))

            if web3.is_connected():
                connection_msg = f"{self.current_time()} 成功连接到 Humanity Protocol"
                connection_msg += f" (使用代理: {proxy})" if proxy else " (直连)"
                print(Fore.GREEN + connection_msg)
                return web3
        except Exception as e:
            print(Fore.RED + f"连接错误: {str(e)}")
            return None

    def claim_rewards(self, private_key, web3, contract):
        """尝试领取奖励"""
        try:
            account = web3.eth.account.from_key(private_key)
            sender_address = account.address
            genesis_claimed = contract.functions.userGenesisClaimStatus(sender_address).call()
            current_epoch = contract.functions.currentEpoch().call()
            buffer_amount, claim_status = contract.functions.userClaimStatus(sender_address, current_epoch).call()

            if (genesis_claimed and not claim_status) or (not genesis_claimed):
                print(Fore.GREEN + f"正在为地址 {sender_address} 领取奖励")
                self.process_claim(sender_address, private_key, web3, contract)
            else:
                print(Fore.YELLOW + f"地址 {sender_address} 当前纪元 {current_epoch} 的奖励已领取")

        except Exception as e:
            print(Fore.RED + f"处理地址 {sender_address} 时发生错误: {str(e)}")

    def process_claim(self, sender_address, private_key, web3, contract):
        """处理领取奖励的交易"""
        try:
            gas_amount = contract.functions.claimReward().estimate_gas({
                'chainId': web3.eth.chain_id,
                'from': sender_address,
                'gasPrice': web3.eth.gas_price,
                'nonce': web3.eth.get_transaction_count(sender_address)
            })
            
            transaction = contract.functions.claimReward().build_transaction({
                'chainId': web3.eth.chain_id,
                'from': sender_address,
                'gas': gas_amount,
                'gasPrice': web3.eth.gas_price,
                'nonce': web3.eth.get_transaction_count(sender_address)
            })
            
            signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print(Fore.GREEN + f"地址 {sender_address} 交易成功，交易哈希: {web3.to_hex(tx_hash)}")

        except Exception as e:
            print(Fore.RED + f"处理地址 {sender_address} 的交易时发生错误: {str(e)}")

    def run(self):
        """运行主循环"""
        print(Fore.CYAN + f"{self.current_time()} L先生------------------QQ214376358")
        print(Fore.CYAN + "脚本已启动，开始执行领取操作...")

        while True:
            try:
                # 加载账号数据
                accounts_data = self.load_accounts_data()
                
                # 为每个账号执行操作
                for account in accounts_data:
                    # 为每个账号建立独立的连接
                    web3 = self.setup_blockchain_connection(account['proxy'])
                    if not web3:
                        print(Fore.RED + "连接失败，跳过当前账号...")
                        continue
                    
                    # 设置合约
                    contract = web3.eth.contract(
                        address=Web3.to_checksum_address(self.contract_address), 
                        abi=self.contract_abi
                    )
                    
                    # 执行领取操作
                    self.claim_rewards(account['private_key'], web3, contract)
                
                print(Fore.CYAN + f"{self.current_time()} 本轮领取完成，等待6小时后继续运行...")
                time.sleep(6 * 60 * 60)  # 6小时

            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n程序已停止运行")
                sys.exit(0)
            except Exception as e:
                print(Fore.RED + f"发生错误: {str(e)}")
                time.sleep(60)  # 发生错误时等待1分钟后继续

if __name__ == "__main__":
    bot = HumanityProtocolBot()
    bot.run()
