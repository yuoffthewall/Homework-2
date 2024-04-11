# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

path: tokenB-> tokenA-> tokenD-> tokenC-> tokenB, tokenB balance=20.129888944077447
tokenB->tokenA, amountIn = 5, amountOut = 5.655321988655323
tokenA->tokenD, amountIn = 5.655321988655323, amountOut = 2.458781317097934
tokenD->tokenC, amountIn = 2.458781317097934, amountOut = 5.0889272933015155
tokenC->tokenB, amountIn = 5.0889272933015155, amountOut = 20.129888944077447

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

The price of an asset is determined by the ratio of tokens in the pool, so when a trader places an order, it will decrease the ratio of one token to another, increasing the price of the token. Slippage is when the quoted price of an asset changes when a trade is executed, resulting in a trader receiving less or more tokens as a result.

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

To ameliorate rounding errors and increase the theoretical minimum tick size for liquidity provision, pairs burn the first MINIMUM_LIQUIDITY pool tokens. For the vast majority of pairs, this will represent a trivial value. The burning happens automatically during the first liquidity provision, after which point the totalSupply is forevermore bounded.

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1)
This provides an incentive for users to increase the supply of token0 and token1 without changing the ratio of token0 and token1.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

The sandwiching occurs by placing one order right before the trade and one right after it. In essence, the attacker will front-run and back-run simultaneously, with the original pending transaction sandwiched in between. Sandwich attacks can increase price slippage for traders, resulting in worse execution prices for their trades. This can lead to higher costs or reduced profits for traders, especially for large trades.

