from pydoc import doc
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib


st.markdown("# Documentation")
st.sidebar.markdown("# Documentation")

header = st.container()
documentation = st.container()

with header:
    st.markdown("""---""")

with documentation:
    st.write(' - Reading & writing to IPFS')

code1 = '''def load_json(path_to_json: str) -> Dict[str, Any]:

    try:
        with open(path_to_json, "r") as config_file:
            conf = json.load(config_file)
            # print(conf)
            return conf

    except Exception as error:
        print(error)
        raise TypeError("Invalid JSON file")


def upload_file(file_path_to_upload, name):
    fileName = name
    m = MultipartEncoder(
        fields={
            "file": (fileName, open(file_path_to_upload, "rb")),
        }
    )

    headers = {
        "pinata_api_key": pinata_public,
        "pinata_secret_api_key": pinata_secret,
        "Content-Type": m.content_type,
    }

    r = requests.post(pinataurl, data=m, headers=headers)

    if r.status_code == 200:
        print("file_uploaded")
        print(r.json()["IpfsHash"])

    else:
        print(r._content)


def upload_image(image_path, name):
    with Path(image_path).open("rb") as fp:
        file_binary = fp.read()

    imageName = name + "_image"
    m = MultipartEncoder(
        fields={
            "file": (imageName, file_binary),
        }
    )

    headers = {
        "pinata_api_key": pinata_public,
        "pinata_secret_api_key": pinata_secret,
        "Content-Type": m.content_type,
    }

    r = requests.post(pinataurl, data=m, headers=headers)

    if r.status_code == 200:
        print("image_uploaded")
        print(r.json())
        return r.json()["IpfsHash"]
    else:
        print(r._content)


def write_file(context, image):

    name = context["name"]
    imageStream = io.BytesIO(image.getvalue())
    imageFile = Image.open(imageStream)
    imageFile.save(f"./cars/{name}.jpeg")
    ipfs_img_hash = upload_image(f"./cars/{name}.jpeg", name=name)
    if ipfs_img_hash:
        context["image"] = "ipfs://" + ipfs_img_hash + f"/{name}_image.jpeg"
        json_object = json.dumps(context, indent=4)
        with open(f"./cars/{name}.json", "w") as outfile:
            outfile.write(json_object)


def upload_data(name):
    ipfs_hash = upload_file(
        file_path_to_upload=f"./cars/{name}.json",
        name=name,
    )
    return ipfs_hash'''
with documentation:
    st.code(code1, language='solidity')
    st.markdown("""---""")

with documentation:
    st.write(' - Tokenizing user input data')

code2 = '''pragma solidity ^0.8.4;

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
}'''
with documentation:
    st.code(code2, language='solidity')
    st.markdown("""---""")

with documentation:
    st.write(' - Adding vehicle to the ledger post uploading to IPFS')

code3 = '''pragma solidity ^0.8.4;

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
}'''

with documentation:
    st.code(code3, language='solidity')
    st.markdown('''---''')