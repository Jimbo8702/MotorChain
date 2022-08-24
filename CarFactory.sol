// SPDX-License-Identifier: MIT
//project 3 contract
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyCarFactory is
    ERC721,
    ERC721Enumerable,
    ERC721URIStorage,
    Pausable,
    Ownable,
    ERC721Burnable
{
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    constructor() ERC721("Test contract1", "DDC") {
        approvedForMint[msg.sender] == true;
    }

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    mapping(string => bool) vinUsed;
    mapping(string => bool) uriUsed;
    mapping(uint256 => address) tokenIdToOwner;
    mapping(uint256 => string) tokenIdToUri;
    mapping(uint256 => string) tokenIdToVin;
    mapping(address => bool) approvedForMint;

    modifier onlyApproved() {
        require(approvedForMint[msg.sender] == true, "Not approved!");
        _;
    }

    function mint(
        address to,
        string memory uri,
        string memory vin
    ) public onlyApproved {
        require(!vinUsed[vin], "vin already in use");
        require(!uriUsed[uri], "uri already in use");
        uint256 tokenId = _tokenIdCounter.current();
        tokenIdToOwner[tokenId] = to;
        _tokenIdCounter.increment();
        vinUsed[vin] = true;
        uriUsed[uri] = true;
        tokenIdToUri[tokenId] = uri;
        tokenIdToVin[tokenId] = vin;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal override(ERC721, ERC721Enumerable) whenNotPaused {
        tokenIdToOwner[tokenId] = to;
        super._beforeTokenTransfer(from, to, tokenId);
    }

    // The following functions are overrides required by Solidity.

    function _burn(uint256 tokenId)
        internal
        override(ERC721, ERC721URIStorage)
        onlyOwner
    {
        super._burn(tokenId);
        string memory uri = tokenIdToUri[tokenId];
        string memory vin = tokenIdToVin[tokenId];
        vinUsed[vin] = false;
        uriUsed[uri] = false;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function setApproveForMint(address _minter) public onlyOwner {
        approvedForMint[_minter] = true;
    }

    function getUriAndVin(uint256 tokenId)
        public
        view
        onlyOwner
        returns (string memory, string memory)
    {
        string memory uri = tokenIdToUri[tokenId];
        string memory vin = tokenIdToVin[tokenId];
        return (uri, vin);
    }
}
