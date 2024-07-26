// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

//imports the token from OpenZeppelin
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";

//creates a new contract for a new token. Its an instance of the ERC20 standard.
//It extends the ERC20 contract
contract LW3Token is ERC20 {
    //creates a constructor function. This is called when the contract is first deployed
    constructor(string memory _name, string memory _symbol) 
    //initializes the new ERC20 token
    ERC20(_name, _symbol){
    //uses the internal ERC20 function '_mint'
    // _mint takes two arguments (an address to mint to, the amount of tokens to mint) 
        _mint(msg.sender, 10 * 10 ** 18);
    //msg.sender is a EVM global variable which is the address which made the transaction
    // 10 * 10 ** 18 (10 ^ 18) is used because solidity does not support floating numbers 
    }
}
