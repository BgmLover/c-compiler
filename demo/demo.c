int fact(int i){
    if(i<=1){
    return 1;
    }
    else{
    return i*fact(i-1);
    }
}

int main(){
    int a[5];
    int i;
    for(i=0;i<5;i++){
    a[i]=i;}
    return a;
}

