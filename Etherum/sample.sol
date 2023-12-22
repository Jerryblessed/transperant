// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HelloWorld {
    string public message;

    // Function to set the message
    function setMessage(string memory _newMessage) public {
        message = _newMessage;
    }

    // Function to get the message
    function getMessage() public view returns (string memory) {
        return message;
    }
}
