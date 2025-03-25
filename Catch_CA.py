import re
import time

from datetime import datetime, date
from wxauto import WeChat
import requests
import base58

# 配置参数
WECHAT_GROUP_NAME = "your-group"  # 要监听的微信群名称
TELEGRAM_BOT_TOKEN = "BOT_TOKEN"
TELEGRAM_CHAT_ID = "CHAT_ID"

# 存储已发现的合约地址
found_addresses = set()
current_date = date.today()  # 记录当前日期
# 多链合约地址正则表达式
ETH_ADDRESS_REGEX = r"0x[a-fA-F0-9]{40}"  # 以太坊/币安智能链等
SOL_ADDRESS_REGEX = r"[1-9A-HJ-NP-Za-km-z]{32,44}"  # Solana地址（Base58编码）

def is_valid_solana_address(address):
    """验证是否为有效的SOL地址"""
    try:
        decoded = base58.b58decode(address)
        return len(decoded) == 32  # SOL地址解码后应为32字节
    except:
        return False

def send_telegram_message(text):
    """通过Telegram Bot发送消息"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        print(f"Telegram消息发送成功: {text}")
    except Exception as e:
        print(f"Telegram消息发送失败: {e}")

def extract_contract_addresses(text):
    """从文本中提取多链合约地址"""
    addresses = []
    
    # 提取以太坊/币安智能链地址
    eth_addresses = re.findall(ETH_ADDRESS_REGEX, text)
    addresses.extend(eth_addresses)
    
    # 提取并验证SOL地址
    potential_sol_addresses = re.findall(SOL_ADDRESS_REGEX, text)
    for addr in potential_sol_addresses:
        if is_valid_solana_address(addr):
            addresses.append(addr)
    
    return addresses

def identify_chain_type(address):
    """识别地址所属的区块链"""
    if address.startswith("0x"):
        return "ETH/BSC"  # 以太坊或币安智能链
    else:
        return "SOL"  # Solana

def check_date_change():
    """检查日期是否变化，如果变化则清空found_addresses"""
    global current_date, found_addresses
    today = date.today()
    if today != current_date:
        print(f"日期从 {current_date} 变为 {today}，清空已存储的合约地址")
        found_addresses = set()
        current_date = today
        
        
def monitor_wechat_group():
    """监听微信群消息"""
    wx = WeChat()
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"开始监听微信群 '{WECHAT_GROUP_NAME}' - {today}")
    listen_list = [
    WECHAT_GROUP_NAME
    ]
    # 获取初始消息作为基准
    for i in listen_list:
        wx.AddListenChat(who=i)
    
    while True:
        try:
            check_date_change()
            # 获取新消息（修改为使用GetMessage方法）
            msgs = wx.GetListenMessage()
            
            # 处理新消息（调整消息结构处理方式）
            for chat in msgs:
                # 检查消息对象类型
                one_msgs=msgs.get(chat)
                for msg in one_msgs:
                    if msg.type == 'sys':
                        continue
                    content=msg.content
                
                    # 提取地址的逻辑保持不变
                    addresses = extract_contract_addresses(content)
                    sender=msg.sender
                    for addr in addresses:
                        addr_lower = addr.lower() if addr.startswith("0x") else addr
                        if addr_lower not in found_addresses:
                            found_addresses.add(addr_lower)
                            chain_type = identify_chain_type(addr)
                            print(f"发现新合约地址 ({chain_type}): {addr}")
                            
                            message = (
                                f"*合约地址*: `{addr}`\n"
                                f"⚠️ 检测到新合约地址\n\n"
                                f"*链类型*: {chain_type}\n"
                                f"*群组*: {WECHAT_GROUP_NAME}\n"
                                f"*时间*: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                                f"*发送者*: {sender}\n"
                            )
                            send_telegram_message(message)
                
            time.sleep(1)
            
        except Exception as e:
            print(f"发生错误: {e}")
            time.sleep(30)
            continue

if __name__ == "__main__":
    monitor_wechat_group()