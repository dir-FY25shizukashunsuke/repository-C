import { User, UserDatabase } from './types';

export class UserManager {
  private database: UserDatabase;

  constructor(database: UserDatabase) {
    this.database = database;
  }

  /**
   * ユーザーを追加する
   */
  addUser(user: User): void {
    this.database.users.push(user);
  }

  /**
   * ユーザーを削除する
   */
  deleteUser(userId: string): boolean {
    const initialLength = this.database.users.length;
    this.database.users = this.database.users.filter(user => user.id !== userId);
    return this.database.users.length < initialLength;
  }

  /**
   * ユーザーをIDで検索
   */
  getUserById(userId: string): User | undefined {
    return this.database.users.find(user => user.id === userId);
  }

  /**
   * すべてのユーザーを取得
   */
  getAllUsers(): User[] {
    return [...this.database.users];
  }

  /**
   * ユーザー数を取得
   */
  getUserCount(): number {
    return this.database.users.length;
  }
}
