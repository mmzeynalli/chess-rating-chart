# chess-rating-chart
Chart your rating of Lichess or Chess.com

Project was heavily inspired by [sciencepal][https://github.com/sciencepal/sciencepal], transformed code to Github Actions and added LiChess support.
Code structure is inspired by [gautamkrishnar][https://github.com/gautamkrishnar/blog-post-workflow]

## How to use

1. Star this repo 😉 
2. Add the following section to YOUR **README.md** file, you can give whatever title you want. Use right comments in your readme and workflow will replace this comment with graph.
   - Use `<!-- START_RATING_GRAPH:chess.com --><!-- END_RATING_GRAPH:chess.com -->` to show your Chess.com graph
   - Use `<!-- START_RATING_GRAPH:lichess --><!-- END_RATING_GRAPH:lichess -->` to show your Lichess.org graph
   - You can use both of them together, like I did in this readme.

    ```markdown
    # Blog posts
    <!-- START_RATING_GRAPH:chess.com -->
    <!-- END_RATING_GRAPH:chess.com -->
    ```

3. Create a folder named `.github` and create a `workflows` folder inside it, if it doesn't exist.
4. Create a new file named `chess-rating-graph.yml` with the following contents inside the workflows folder:

    ```yaml
    name: Update chess rating graph
    on:
      schedule: # Run workflow automatically
        - cron: '0 0 * * *' # Runs every day, at 00:00 UTC
    permissions:
      contents: write # To write the generated contents to the readme
    
    jobs:
      update-ratings-graph:
        name: Update this repo's README chess rating graph
        runs-on: ubuntu-latest
        steps:
          - name: Checkout
            uses: actions/checkout@v4
          - name: Update chart
            uses: mmzeynalli/chess-rating-chart@v1
            with:
              GH_TOKEN: ${{ secrets.GH_TOKEN }}
              CHESS_COM_USERNAME: your_chess_com_username
              LICHESS_USERNAME: your_lichess_username
    ```

5. Replace your usernames. You can give one of them, no need for both.
6. Go to repository settings, Click on Actions > General. Update the "Workflow permissions" to "Read and write permissions". Click on save.
   ![Workflow permissions](https://github.com/gautamkrishnar/blog-post-workflow/assets/8397274/26d4c089-dc58-4309-b65a-2acb9a3c08ba)
7. Wait for it to run automatically, or you can also trigger it manually to see the result instantly.

## Extra arguments

So, you can pass multiple arguments to the `with` key:

1. `CHESS_COM_TIME_CLASS`: which time class games of Chess.com to chart. Available values: `"daily", "rapid", "blitz", "bullet"`. Default: `"blitz"`
2. `LICHESS_TIME_CLASS`: which time class games of Lichess to chart. Available values: `"ultraBullet", "bullet", "blitz", "rapid", "classical", "correspondence"`. Default: `"blitz"`
3. `LAST_N_GAMES`: How many last game to consider for plotting. Deafult value: `100`
4. `RATING_CHART_HEIGHT`: Height of ascii plot. Default: `20`
5. `PUSH_BRANCH_NAME`: To which branch to push. Default: main branch (`main` or `master`).
6. `COMMIT_BY_ME`: Whether graph update commit should be from users name or github-action bot's. Default value: `False`.
7. `COMMIT_MESSAGE`: Update commit message. Default: `""`

Here is my rating data:

<!-- START_SECTION:chess.com -->
Chess.com rating chart for the last 100 games:

 2470.00  ┤
 2449.19  ┼╮    ╭╮╭╮
 2428.38  ┤╰╮   │╰╯│      ╭╮
 2407.57  ┤ │  ╭╯  ╰╮╭────╯╰─────╮                          ╭──────╮
 2386.76  ┤ ╰╮╭╯    ╰╯           │╭╮ ╭──────╮╭╮         ╭───╯      ╰──╮                           ╭───╮
 2365.95  ┤  ││                  ╰╯╰─╯      ╰╯╰───╮  ╭──╯             ╰────────────────────╮    ╭─╯   │
 2345.14  ┤  ╰╯                                   ╰──╯                                     ╰────╯     │
 2324.33  ┤                                                                                           │
 2303.52  ┤                                                                                           │
 2282.71  ┤                                                                                           │
 2261.90  ┤                                                                                           │
 2241.10  ┤                                                                                           │
 2220.29  ┤                                                                                           │
 2199.48  ┤                                                                                           │
 2178.67  ┤                                                                                           │
 2157.86  ┤                                                                                           │
 2137.05  ┤                                                                                           │
 2116.24  ┤                                                                                           │
 2095.43  ┤                                                                                           │
 2074.62  ┤                                                                                           │   ╭───
 2053.81  ┤                                                                                           │ ╭─╯
 2033.00  ┤                                                                                           ╰─╯
<!-- END_SECTION:chess.com -->


<!-- START_SECTION:lichess -->
Lichess rating chart for the last 100 games:

 2631.00  ┤                                         ╭╮
 2627.90  ┤                                       ╭╮││
 2624.81  ┤                                      ╭╯╰╯╰╮        ╭╮
 2621.71  ┤                                    ╭╮│    │        ││
 2618.62  ┤                                    │╰╯    ╰╮      ╭╯╰╮ ╭╮╭╮            ╭╮
 2615.52  ┤                                   ╭╯       ╰╮     │  ╰╮││││            ││           ╭╮╭╮╭╮
 2612.43  ┤                                   │         ╰╮    │   ││╰╯│     ╭╮     │╰╮ ╭╮       │╰╯│││   ╭╮  ╭
 2609.33  ┤                                  ╭╯          │   ╭╯   ╰╯  ╰╮╭╮  │╰╮   ╭╯ ╰╮││ ╭╮   ╭╯  ╰╯╰╮  ││  │
 2606.24  ┤                                 ╭╯           ╰╮  │         ╰╯╰╮╭╯ ╰╮╭─╯   ╰╯╰╮│╰╮╭─╯      ╰╮╭╯╰╮╭╯
 2603.14  ┤                                 │             ╰╮╭╯            ╰╯   ││        ╰╯ ╰╯         ││  ││
 2600.05  ┤                                ╭╯              ││                  ╰╯                      ╰╯  ╰╯
 2596.95  ┤               ╭╮               │               ╰╯
 2593.86  ┤               │╰╮             ╭╯
 2590.76  ┤              ╭╯ ╰╮            │
 2587.67  ┤          ╭╮  │   │           ╭╯
 2584.57  ┤        ╭╮│╰╮ │   │ ╭╮        │
 2581.48  ┤      ╭╮│╰╯ ╰─╯   ╰╮│╰╮ ╭╮   ╭╯
 2578.38  ┤      │╰╯          ╰╯ ╰╮││ ╭╮│
 2575.29  ┤╭╮   ╭╯                ││╰╮│╰╯
 2572.19  ┤│╰╮╭╮│                 ╰╯ ╰╯
 2569.10  ┼╯ ╰╯╰╯
 2566.00  ┤
<!-- END_SECTION:lichess -->
