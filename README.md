## CW20 -> Native Denom

This tool will allow you to convert a CW20 -> a chains native denomination via a x/tokenfactory module in the SDK.

### Usage
```bash
cp .env.example .env
# edit .env with the data you want for your CW20 convert.

sh script1.sh
# wait for it to save all to CW20s/ folder
# For now only standard CW20s are supported.
# For forked support, contact 
#- Discord: Reece#3307 / Twitter: @Reecepbcups_ 

pip install -r requirements/requirements.txt
python3 script2.py

# Done! Double check balance.json looks right and then finally mint the tokens to their addresses
sh factory_mint.sh
```

### note
You could also update the TOKEN_FACTORY_MINT_COMMAND (.env.example) to be a `simd add-genesis-account` command as well (If you want to move your CW20 to its own chain)