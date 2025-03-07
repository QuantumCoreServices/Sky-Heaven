// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AITradingBot {
    address public owner;
    mapping(address => uint) public balances;

    event TradeExecuted(string action, uint amount, string symbol);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function trade(string memory action, uint amount, string memory symbol) public onlyOwner {
        emit TradeExecuted(action, amount, symbol);
    }

    function withdraw() public onlyOwner {
        payable(owner).transfer(address(this).balance);
    }
}
