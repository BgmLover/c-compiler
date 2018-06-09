int fact(int i){
    if(i<=1){
    return 1;
    }
    else{
    return i*fact(i-1);
    }
}

int main(){
    int i;
    int j = read();
    for(i = 0; i<j; i++){
        print(fact(i));
    }
    return 0;
}

