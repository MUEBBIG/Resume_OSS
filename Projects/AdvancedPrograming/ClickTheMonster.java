import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class Game extends JFrame {
    private int playerHealth = 5; // 플레이어 체력
    private int count = 0; // 잡은 몬스터 수
    private JLabel healthLabel; // 체력을 표시하는 레이블
    private JLabel describeLabel; // 몬스터, 아이템을 설명하는 레이블

    public Game() {
        setTitle("몬스터를 잡아라!"); // 프레임 제목 설정
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // 프로그램 종료 설정
        Container c = getContentPane(); // 콘텐츠 팬 설정
        c.setLayout(null); // 레이아웃 매니저 설정

        // 체력을 표시하는 레이블 생성
        healthLabel = new JLabel("플레이어 체력: " + playerHealth);
        healthLabel.setSize(100, 25); // 크기 설정
        healthLabel.setLocation(10, 10); // 위치 설정
        healthLabel.setForeground(Color.BLUE);
        c.add(healthLabel); // 콘텐츠 팬에 체력 레이블 추가
        
        // 노말 몬스터를 설명하는 레이블 생성
        describeLabel = new JLabel("(^･ω･^)  : 공격력 0");
        describeLabel.setSize(120, 25); // 크기 설정
        describeLabel.setLocation(10, 380); // 위치 설정
        c.add(describeLabel); // 콘텐츠 팬에 설명 레이블 추가
        
        // 공격 몬스터를 설명하는 레이블 생성
        describeLabel = new JLabel("(^･д･^)  : 공격력 1");
        describeLabel.setSize(120, 25); // 크기 설정
        describeLabel.setLocation(10, 405); // 위치 설정
        c.add(describeLabel); // 콘텐츠 팬에 설명 레이블 추가
        
        // 아이템을 설명하는 레이블 생성
        describeLabel = new JLabel("Item  : 플레이어 체력 +1");
        describeLabel.setSize(140, 25); // 크기 설정
        describeLabel.setLocation(10, 430); // 위치 설정
        c.add(describeLabel); // 콘텐츠 팬에 설명 레이블 추가

        // 일정 주기마다 몬스터와 아이템을 이동시키기 위한 타이머 생성 및 시작
        Timer timer = new Timer(100, new ActionListener() { // 100ms (0.1초) 간격으로, ActionListenr을 통해.
            @Override
            public void actionPerformed(ActionEvent e) { // 0.1초 간격으로 ActionEvent 발생, ...
                moveMonstersAndItems(); // 메소드 호출
            }
        });
        timer.start();

        // 초기에 몬스터와 아이템을 생성하여 콘텐츠 팬에 추가
        for (int i = 0; i < 10; i++) {
            c.add(createMonster(new AttackMonster()));
            c.add(createMonster(new NormalMonster()));
            c.add(createItem());
        }

        setSize(500, 500); // 프레임 크기 설정
        setVisible(true); // 프레임을 보이도록 설정
    }

    // 몬스터 레이블을 생성하는 메서드
    private JLabel createMonster(Monster monster) {
        JLabel label = new JLabel(monster.getIcon(), SwingConstants.CENTER); // 아이콘과 가운데 정렬된 레이블 생성
        label.setSize(60, 25); // 크기 설정
        label.setBackground(monster.getColor()); // 배경색 설정
        label.setOpaque(true); // 불투명하게 설정
        label.addMouseListener(new MonsterMouseAdapter(monster)); // 몬스터에 대한 마우스 리스너 추가
        label.setLocation((int) (Math.random() * 450), (int) (Math.random() * 450)); // 무작위 위치 설정
        return label; // 생성된 몬스터 레이블 반환
    }

    // 아이템 레이블을 생성하는 메서드
    private JLabel createItem() {
        JLabel item = new JLabel("Item", SwingConstants.CENTER); // "Item"과 가운데 정렬된 레이블 생성
        item.setSize(60, 25); // 크기 설정
        item.setBackground(Color.GREEN); // 배경색 설정
        item.setOpaque(true); // 불투명하게 설정
        item.addMouseListener(new ItemMouseAdapter()); // 아이템에 대한 마우스 리스너 추가
        item.setLocation((int) (Math.random() * 450), (int) (Math.random() * 450)); // 무작위 위치 설정
        return item; // 생성된 아이템 레이블 반환
    }

    // 몬스터와 아이템을 이동시키는 메서드
    private void moveMonstersAndItems() {
        for (java.awt.Component component : getContentPane().getComponents()) { // 콘텐츠 팬에 추가된 모든 컨포넌트 가져오기
            if (component instanceof JLabel) { // 컴포넌트가 JLabel 타입이고 ...
                JLabel label = (JLabel) component;
                // 레이블의 텍스트가 각 몬스터, Item과 일치한다면 이동을 처리
                if (label.getText().equals("Item") || label.getText().equals("(^･д･^)") || label.getText().equals("(^･ω･^)")) {
                    // 아이템 또는 몬스터인 경우
                    int direction = (int) (Math.random() * 4); // 0~4를 랜덤으로 반환 (0: 상, 1: 하, 2: 좌, 3: 우)
                    int step = 7; // 한 번에 이동하는 거리
                    int x = label.getX();
                    int y = label.getY();

                    // 이동 방향에 따라 좌표 조정
                    switch (direction) {
                        case 0: // 상
                            y = Math.max(0, y - step); // y - step의 최소값을 0으로 보장
                            break;
                        case 1: // 하
                            y = Math.min(450, y + step); // y + step의 최대값을 450으로 보장
                            break;
                        case 2: // 좌
                            x = Math.max(0, x - step); // x - step의 최소값을 0으로 보장
                            break;
                        case 3: // 우
                            x = Math.min(450, x + step); // x - step의 최대값을 450으로 보장
                            break;
                    }

                    label.setLocation(x, y); // 새로운 좌표로 레이블 이동
                }
            }
        }

        if (count >= 20) {
            JOptionPane.showMessageDialog(this, "Clear!"); // 목표 수량을 달성한 경우 메시지 출력
            System.exit(0); // 프로그램 종료
        }
    }

    // MouseAdapter를 상속한 몬스터 마우스 어댑터
    class MonsterMouseAdapter extends MouseAdapter {
        private Monster monster;

        public MonsterMouseAdapter(Monster monster) {
            this.monster = monster;
        }

        @Override
        public void mousePressed(MouseEvent e) {
            JLabel lb = (JLabel) e.getSource();

            if (lb.isVisible()) {
            	// 몬스터가 보이는 경우
                if (monster instanceof AttackMonster) {
                    playerHealth--; // 플레이어 체력 감소
                    healthLabel.setText("플레이어 체력: " + playerHealth); // 체력 레이블 업데이트
                    if (playerHealth <= 0) {
                        JOptionPane.showMessageDialog(Game.this, "Game Over"); // 체력이 0 이하인 경우 게임 오버 메시지 출력
                        System.exit(0); // 프로그램 종료
                    }
                }

                lb.setVisible(false); // 몬스터 레이블 숨기기
                count++; // 잡은 몬스터 수 증가
                setTitle("몬스터를 " + count + " 마리 잡았습니다!"); // 프레임 제목 업데이트
            }
        }
    }

    // MouseAdapter를 상속한 아이템 마우스 어댑터
    class ItemMouseAdapter extends MouseAdapter {
        @Override
        public void mousePressed(MouseEvent e) {
            JLabel lb = (JLabel) e.getSource();
            if (lb.isVisible()) {
            	// 아이템이 보이는 경우
                playerHealth++; // 플레이어 체력 증가
                healthLabel.setText("플레이어 체력: " + playerHealth); // 체력 레이블 업데이트
                lb.setVisible(false); // 아이템 레이블 숨기기
            }
        }
    }

    // 추상 클래스 Monster 정의
    abstract class Monster {
        public abstract String getIcon(); // 몬스터 아이콘 반환
        public abstract Color getColor(); // 몬스터 배경색 반환
    }

    // 공격 몬스터 클래스 정의
    class AttackMonster extends Monster {
        @Override
        public String getIcon() {
            return "(^･д･^)"; // 공격 몬스터 아이콘 반환
        }

        @Override
        public Color getColor() {
            return Color.RED; // 공격 몬스터 배경색 반환
        }
    }

    // 일반 몬스터 클래스 정의
    class NormalMonster extends Monster {
        @Override
        public String getIcon() {
            return "(^･ω･^)"; // 일반 몬스터 아이콘 반환
        }

        @Override
        public Color getColor() {
            return Color.CYAN; // 일반 몬스터 배경색 반환
        }
    }

    // 메인 메서드
    public static void main(String[] args) {
        new Game(); // 게임 인스턴스 생성
    }
}
