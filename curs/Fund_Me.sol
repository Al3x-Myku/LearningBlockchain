// SPDX-License-Identifier: MIT
pragma solidity >=0.8.16;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    address public owner;
    constructor() {
         owner = msg.sender;
    }
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;

    function Fund() public payable {
        // $50
       // uint256 minimumUSD = 50 * 10 ** 18; //10 la a 18 ppentru conversie gwei
       // if(msg.value < minimumUSD) revert("not enough ether");
        //sau require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
        //^^^^^^^^^^^^^^^ msg.sender si msg.value sunt keywords referitoare la cel ce foloste contractul
        // conversie ETH -> USD
        // luam informatii de la un "Oraclu"

    }
    //urm 2 functii nu merg ca nu sunt pe networkul potrivit
    function getVersion() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419);
        return priceFeed.version();
        //ori deploy pe un testnet sau folosesti un mockOracle
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419);
        (
         uint80 roundId,
         int256  answer,
           uint256 startedAt,
           uint256 updatedAt,
           uint80 answeredInRound
        ) =  priceFeed.latestRoundData();
        return uint256(answer * 10000000);
    }

    function getConversionrate(uint256 _amount)public view returns (uint256) {
        uint256 price = getPrice();
        uint256 ethprice = _amount * price;
        return ethprice / 10000000;
    }

    modifier doarOwner {
        require(msg.sender == owner);
        _;
    }

    function withdraw() payable doarOwner public {
        //called doar de owner
        // require(msg.sender == owner);
        payable (msg.sender).transfer(address(this).balance);
        for(uint256 i = 0; i < funders.length; i++){
            address funder = funders[i];
            addressToAmountFunded[funder] = 0;
            //seteaza inapoi la 0
        }
        funders = new address[](0);
    }

}