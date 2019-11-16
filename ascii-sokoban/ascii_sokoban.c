#include<stdio.h>       /** SIMPLE  C SOKOBAN | Gameplay: https://gfycat.com/ashamedordinarybluejay **/
#include<string.h>      /** Made by Lorand Horvath 2019 | ??: https://en.wikipedia.org/wiki/Sokoban **/

int l = 0;                  //current level number
int main(){
    int x, y, k;            // loop variables
    char target[10][10];    // shadow level only with targets
    int target_num = 0;     // number of targets
    int target_ok = 0;      // completed targets
    int pos_x, pos_y;       // player position
    char level[3][10][10];  // levels

    int l_max = 3;          // the levels ( # = wall, o = ball, + = target, X = player )
    strcpy(level[0][0],"##########"); strcpy(level[1][0],"##########"); strcpy(level[2][0],"##########");
    strcpy(level[0][1],"#    + + #"); strcpy(level[1][1],"#        #"); strcpy(level[2][1],"#+++#   X#");
    strcpy(level[0][2],"#    o   #"); strcpy(level[1][2],"# X o  + #"); strcpy(level[2][2],"##o # ####");
    strcpy(level[0][3],"#    o   #"); strcpy(level[1][3],"#  #######"); strcpy(level[2][3],"##  #  #+#");
    strcpy(level[0][4],"#+o      #"); strcpy(level[1][4],"# o#    +#"); strcpy(level[2][4],"# o  #  o#");
    strcpy(level[0][5],"#    X   #"); strcpy(level[1][5],"#  #  ####"); strcpy(level[2][5],"# o ###  #");
    strcpy(level[0][6],"#        #"); strcpy(level[1][6],"# +#  o  #"); strcpy(level[2][6],"#  #   +##");
    strcpy(level[0][7],"#  ####o #"); strcpy(level[1][7],"#  #   # #"); strcpy(level[2][7],"#    o# # ");
    strcpy(level[0][8],"#   +    #"); strcpy(level[1][8],"#        #"); strcpy(level[2][8],"####    # ");
    strcpy(level[0][9],"##########"); strcpy(level[1][9],"##########"); strcpy(level[2][9],"   ###### ");

    // search for the player and targets
    for(x=0; x<10; x++){
        for(y=0; y<10; y++){
            target[x][y] = ' ';
            if(level[l][x][y] == '+'){ target[x][y] = '+'; level[l][x][y] = ' '; target_num++; }
            if(level[l][x][y] == 'X'){ pos_x = x; pos_y = y; level[l][x][y] = ' '; }
    }}

    /* ################################ GAMELOOP ################################ */
    while(1){

        /**************** count ok targets ****************/
        target_ok = 0;
        for(x=0; x<10; x++){
            for(y=0; y<10; y++){
                if(target[x][y] == '+' && level[l][x][y] == 'o'){
                    target_ok++;
                }
        }}
        /**************** draw level ****************/
        system("cls"); printf("Level:   %d / %d   Move the balls on the targets\n", l+1, l_max );
        printf("Targets: %d / %d              Move: W A S D keys \n", target_ok, target_num);
        printf("                              Restart level: R\n");
        for(x=0; x<10; x++){
            for(k=0; k<2; k++) {
                for(y=0; y<10; y++){
                    if( x == pos_x  && y == pos_y){
                        printf("XX");
                    } else {
                        if ( target[x][y] == '+' && level[l][x][y] == ' ') {
                            printf("..");
                        } else if(level[l][x][y] == 'o'){
                            if(k==0){ printf("/\\"); } else { printf("\\/"); }
                        } else{
                            printf("%c%c",level[l][x][y],level[l][x][y]);
                        }
                    }
                }
                if(k==0) printf("\n");
            }
            printf("\n");
        }
        /**************** completed? ****************/
        if(target_ok == target_num){
            if( l == l_max-1) { printf("\nGAME COMPLETED! Press ENTER to exit."); getchar(); exit(0); }
            printf("\nLEVEL COMPLETED! Press ENTER to continue."); getchar(); l++; main();
        }
        /**************** move player ****************/
        char irany = getch();
        int xcheck, ycheck;
        switch(irany){
            case 'w': xcheck=-1; ycheck=0; break;           // move up
            case 'a': xcheck=0; ycheck=-1; break;           // move left
            case 's': xcheck=1; ycheck=0; break;            // move down
            case 'd': xcheck=0; ycheck=1; break;            // move right
            case 'r': main(); break;                        // restart level
            case 'n': if(l<l_max-1) { l++; main(); } break;   // next level
        }

        // if the cell in front of us contains a ball and in front of the ball there is an empty space
        if( level[l][pos_x+xcheck][pos_y+ycheck] == 'o' && level[l][pos_x+2*xcheck][pos_y+2*ycheck] == ' '){
            // move box and player
            level[l][pos_x+xcheck][pos_y+ycheck] = ' ';
            level[l][pos_x+2*xcheck][pos_y+2*ycheck] = 'o';
            pos_x+=xcheck;
            pos_y+=ycheck;
        }

        // if the cell in front of us is empty
        if( level[l][pos_x+xcheck][pos_y+ycheck] == ' ' ){
            pos_x+=xcheck;  // move player
            pos_y+=ycheck;
        }
    }
return 0;
}