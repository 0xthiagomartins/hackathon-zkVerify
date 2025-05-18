# Deploy na Taraxa testnet
forge script script/Deploy.s.sol --rpc-url $TARAXA_RPC_URL --private-key $PRIVATE_KEY --broadcast

# Deploy no zkVerify testnet
forge script script/Deploy.s.sol --rpc-url $ZKVERIFY_RPC_URL --private-key $PRIVATE_KEY --broadcast