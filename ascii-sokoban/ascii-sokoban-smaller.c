#include<stdio.h>  /** SIMPLE C SOKOBAN in 50 lines of code         Made by Lorand Horvath 2020 **/
#include<string.h> /** -------------------------------------------------------------------------**/
#define g() getch() // redefine getch() as g()
#define p(f_, ...) printf((f_), ##__VA_ARGS__)
#define s(f_, ...) strcpy((f_), ##__VA_ARGS__)
int c = 3, max = 4;   //current level, max num of levels
int main(){ 
    // loop vars | num of targets | completed targets | player pos | level arrays    | shadow level
    int k, x, y,   t_num = 0,       t_ok = 0,           px, py;      char l[max][11][11], t[10][10];
    s(l[0][0],"SOKOBAN   ");s(l[3][0],"  ########");s(l[1][0],"##########");s(l[2][0],"##########");
    s(l[0][1],"----------");s(l[3][1],"###   # +#");s(l[1][1],"#        #");s(l[2][1],"#+++#   x#");
    s(l[0][2],"MOVE: WASD");s(l[3][2],"#+xo  #+o#");s(l[1][2],"# x o  + #");s(l[2][2],"##o # ####");
    s(l[0][3],"RESTART: R");s(l[3][3],"### o+#o #");s(l[1][3],"#  #######");s(l[2][3],"##  #  #+#");
    s(l[0][4],"##########");s(l[3][4],"#+##o #  #");s(l[1][4],"# o#    +#");s(l[2][4],"# o  #  o#");
    s(l[0][5],"#   x   +#");s(l[3][5],"# # + ## #");s(l[1][5],"#  #  ####");s(l[2][5],"# o ###  #");
    s(l[0][6],"#+o    o #");s(l[3][6],"#o  oo+# #");s(l[1][6],"# +#  o  #");s(l[2][6],"#  #   +##");
    s(l[0][7],"#  ####o #");s(l[3][7],"#   +    #");s(l[1][7],"#  #   # #");s(l[2][7],"#    o# # ");
    s(l[0][8],"#   +    #");s(l[3][8],"#        #");s(l[1][8],"#        #");s(l[2][8],"####    # ");
    s(l[0][9],"##########");s(l[3][9],"##########");s(l[1][9],"##########");s(l[2][9],"   ###### ");
    // search player and targets                           ( # =wall, o =ball, + =target, x =player)
    for(k=0; k<100; k++){ t[x=k/10][y=k%10] = ' ';
        if(l[c][x][y] == '+'){ t[x][y] = '+'; l[c][x][y] = ' '; t_num++; }
        if(l[c][x][y] == 'x'){ px = x; py = y; l[c][x][y] = ' ';   }
    } /* GAMELOOP ################################################################ */
    while(1){
        // draw level, and count ok targets -----------------------------------------
        for(k=0; k<25; k++) p("\n");                             // clear screen
        p("Level:   %d / %d\nTargets: %d / %d\n\n", c+1, max, t_ok, t_num ); // info
        for(t_ok = 0, k=0; k<100; k++){ x=k/10; y=k%10;
            if(t[x][y] == '+' && l[c][x][y] == 'o') t_ok++;      // count ok targets
            if( x == px  && y == py) p("x");                     // draw player
            else if(t[x][y] == '+' && l[c][x][y] == ' ') p("."); // draw target
            else p("%c",l[c][x][y]);                             // draw misc
            if( (k+1)%10==0 ) p("\n");                           // print new line
        } // completed? -------------------------------------------------------------
        if(t_ok==t_num){ p("\nCOMPLETED! Enter>"); g(); if(c==max-1) return 0; else c++; main(); }
        // move player --------------------------------------------------------------
        int dir=g(), dx=0, dy=0; 
        if( dir == 'w') { dx=-1; dy=0;  } // up
        if( dir == 'a') { dx=0;  dy=-1; } // left
        if( dir == 's') { dx=1;  dy=0;  } // down
        if( dir == 'd') { dx=0;  dy=1;  } // right
        if( dir == 'r') { main(); }       // restart
        // move ball, if empty behind the ball --------------------------------------
        if( l[c][px+dx][py+dy] == 'o' && l[c][px+2*dx][py+2*dy] == ' '){
            l[c][px+dx][py+dy] =  ' ';   l[c][px+2*dx][py+2*dy] =  'o';
        } // move player, if empty in front of player -------------------------------
        if( l[c][px+dx][py+dy] == ' ' ) { px+=dx; py+=dy; }
    }
}